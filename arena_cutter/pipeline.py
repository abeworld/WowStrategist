from __future__ import annotations

import csv
import json
import sys
from dataclasses import asdict
from html import escape
from pathlib import Path
from typing import Any

import cv2

from arena_cutter import __version__
from arena_cutter.config import CutterConfig, require_profile
from arena_cutter.detector import TemplateBank, score_roi, text_mask
from arena_cutter.segments import (
    ArenaSegment,
    Sample,
    clamp,
    contact_sheet_timestamps,
    format_timestamp,
    sanitize_video_name,
    segment_samples,
)
from arena_cutter.video import (
    FfmpegError,
    analysis_ready_args,
    export_analysis_ready,
    export_stream_copy,
    extract_frame,
    ffmpeg_version,
    ffprobe_version,
    iter_seek_frames,
    iter_sequential_frames,
    probe,
    stream_copy_args,
    verify_clip_decodable,
    write_contact_sheet,
)


def match_record(
    match_number: int,
    source_name: str,
    output_name: str,
    segment: ArenaSegment,
    profile_name: str,
    scan_backend: str,
    export_status: str,
    export_error: str | None,
    actual_clip_duration: float | None,
) -> dict[str, Any]:
    duration = max(0.0, segment.padded_end - segment.padded_start)
    return {
        "match_number": match_number,
        "source_filename": source_name,
        "output_filename": output_name,
        "raw_start_s": segment.raw_start,
        "raw_end_s": segment.raw_end,
        "padded_start_s": segment.padded_start,
        "padded_end_s": segment.padded_end,
        "start_timestamp": format_timestamp(segment.padded_start),
        "end_timestamp": format_timestamp(segment.padded_end),
        "duration_s": duration,
        "actual_clip_duration_s": actual_clip_duration,
        "confidence": segment.confidence,
        "mean_score": segment.mean_score,
        "max_score": segment.max_score,
        "primary_positive_count": segment.primary_positive_count,
        "gladius_positive_count": segment.gladius_positive_count,
        "merged_gaps": [
            {
                "gap_start": gap.gap_start,
                "gap_end": gap.gap_end,
                "gap_seconds": gap.gap_seconds,
            }
            for gap in segment.merged_gaps
        ],
        "truncated_start": segment.truncated_start,
        "truncated_end": segment.truncated_end,
        "detector_profile": profile_name,
        "scan_backend": scan_backend,
        "export_status": export_status,
        "export_error": export_error,
        "warnings": list(segment.warnings),
    }


def write_manifests(output_dir: Path, records: list[dict[str, Any]], run_meta: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fieldnames = list(records[0].keys()) if records else [
        "match_number",
        "source_filename",
        "output_filename",
        "export_status",
    ]
    csv_path = output_dir / "manifest.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["merged_gaps"] = json.dumps(row.get("merged_gaps") or [])
            row["warnings"] = json.dumps(row.get("warnings") or [])
            writer.writerow(row)
    payload = dict(run_meta)
    payload["matches"] = records
    (output_dir / "manifest.json").write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )


def render_review_html(records: list[dict[str, Any]], sheet_relpaths: list[str]) -> str:
    cards: list[str] = []
    for record, sheet in zip(records, sheet_relpaths):
        warnings = ", ".join(escape(str(item)) for item in record.get("warnings") or []) or "none"
        error = record.get("export_error")
        error_html = f"<p class='error'>Export error: {escape(str(error))}</p>" if error else ""
        mp4 = escape(str(record["output_filename"]))
        cards.append(
            f"""
<section class="card">
  <h2>Match {int(record['match_number']):03d}</h2>
  <p>Source {escape(str(record['source_filename']))} ·
     {escape(str(record['start_timestamp']))} – {escape(str(record['end_timestamp']))}
     ({float(record['duration_s']):.1f}s)</p>
  <p>Confidence: {escape(str(record['confidence']))} ·
     mean score {float(record['mean_score']):.3f} ·
     warnings: {warnings}</p>
  {error_html}
  <p><img src="{escape(sheet)}" alt="contact sheet match {int(record['match_number']):03d}"></p>
  <p><a href="../{mp4}">{mp4}</a></p>
</section>
"""
        )
    body = "\n".join(cards) if cards else "<p>No matches detected.</p>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Arena cutter review</title>
  <style>
    body {{ font-family: sans-serif; background: #111; color: #eee; margin: 0; }}
    h1, h2 {{ margin-bottom: 0.3em; }}
    .card {{ margin: 24px; padding: 16px; background: #1b1b1b; border-radius: 8px; }}
    img {{ max-width: 100%; height: auto; }}
    a {{ color: #8cf; }}
    .error {{ color: #f88; }}
  </style>
</head>
<body>
  <h1>Arena cutter review</h1>
  {body}
</body>
</html>
"""


class OutputExistsError(FileExistsError):
    """Raised when a previous run's artifacts exist and --overwrite was not set."""


def output_run_dir(output_root: Path, source: Path) -> Path:
    return Path(output_root) / sanitize_video_name(source.name)


def assert_can_write(run_dir: Path, overwrite: bool) -> None:
    if overwrite or not run_dir.exists():
        return
    has_manifest = (run_dir / "manifest.json").exists() or (run_dir / "manifest.csv").exists()
    has_clips = any(run_dir.glob("match_*.mp4"))
    if has_manifest or has_clips:
        raise OutputExistsError(
            f"output artifacts already exist in {run_dir}; pass --overwrite to replace them"
        )


def refine_from_scores(
    coarse_start: float,
    coarse_end: float,
    samples: list[Sample],
    window: float,
    lo_bound: float | None = None,
    hi_bound: float | None = None,
) -> tuple[float, float]:
    start_lo, start_hi = coarse_start - window, coarse_start + window
    end_lo, end_hi = coarse_end - window, coarse_end + window
    if lo_bound is not None:
        start_lo = max(start_lo, lo_bound)
        end_lo = max(end_lo, lo_bound)
    if hi_bound is not None:
        start_hi = min(start_hi, hi_bound)
        end_hi = min(end_hi, hi_bound)
    def _usable(ts: float) -> bool:
        if lo_bound is not None and ts <= lo_bound:
            return False
        if hi_bound is not None and ts >= hi_bound:
            return False
        return True

    start_hits = [
        sample
        for sample in samples
        if start_lo <= sample.timestamp <= start_hi
        and (sample.positive or sample.borderline)
        and _usable(sample.timestamp)
    ]
    end_hits = [
        sample
        for sample in samples
        if end_lo <= sample.timestamp <= end_hi
        and (sample.positive or sample.borderline)
        and _usable(sample.timestamp)
    ]
    raw_start = start_hits[0].timestamp if start_hits else coarse_start
    raw_end = end_hits[-1].timestamp if end_hits else coarse_end
    if lo_bound is not None:
        raw_start = max(raw_start, lo_bound)
    if hi_bound is not None:
        raw_end = min(raw_end, hi_bound)
    if raw_end < raw_start:
        raw_end = raw_start
    return raw_start, raw_end


def with_refined_bounds(
    segment: ArenaSegment,
    raw_start: float,
    raw_end: float,
    config: CutterConfig,
    duration: float,
) -> ArenaSegment:
    padded_start = clamp(raw_start - config.pre_roll, 0.0, duration)
    padded_end = clamp(raw_end + config.post_roll, 0.0, duration)
    return ArenaSegment(
        raw_start=raw_start,
        raw_end=raw_end,
        padded_start=padded_start,
        padded_end=padded_end,
        confidence=segment.confidence,
        mean_score=segment.mean_score,
        max_score=segment.max_score,
        primary_positive_count=segment.primary_positive_count,
        gladius_positive_count=segment.gladius_positive_count,
        sample_count=segment.sample_count,
        merged_gaps=list(segment.merged_gaps),
        truncated_start=segment.truncated_start or padded_start == 0.0 and raw_start - config.pre_roll < 0,
        truncated_end=segment.truncated_end or padded_end == duration and raw_end + config.post_roll > duration,
        warnings=list(segment.warnings),
    )


def _sample_from_roi_score(score) -> Sample:
    return Sample(
        timestamp=float(score.timestamp or 0.0),
        positive=score.is_positive,
        borderline=score.is_borderline,
        score=score.primary_score,
        winning_template=score.winning_template,
        gladius_present=score.gladius_present,
    )


def _iter_coarse(source: Path, start: float, end: float, config: CutterConfig, source_fps: float):
    roi = config.profile.primary_roi
    if config.scan_backend == "seek":
        return iter_seek_frames(source, start, end, config.scan_interval, roi)
    return iter_sequential_frames(
        source, start, end, config.scan_interval, roi, source_fps=source_fps
    )


def _refine_segment(
    source: Path,
    segment: ArenaSegment,
    config: CutterConfig,
    bank: TemplateBank,
    duration: float,
    ffmpeg_log: list[str],
    source_fps: float,
    lo_bound: float | None = None,
    hi_bound: float | None = None,
) -> ArenaSegment:
    profile = config.profile
    roi = profile.primary_roi
    window = config.refine_window_seconds
    start_lo = clamp(segment.raw_start - window, 0.0, duration)
    start_hi = clamp(segment.raw_start + window, 0.0, duration)
    end_lo = clamp(segment.raw_end - window, 0.0, duration)
    end_hi = clamp(segment.raw_end + window, 0.0, duration)
    ffmpeg_log.append(
        f"refine start {start_lo:.3f}-{start_hi:.3f} end {end_lo:.3f}-{end_hi:.3f} "
        f"interval={config.refine_interval} crop={roi.as_ffmpeg_crop()}"
    )
    refined_samples: list[Sample] = []
    windows = [(start_lo, start_hi)]
    if end_lo > start_hi:
        windows.append((end_lo, end_hi))
    else:
        windows = [(start_lo, max(start_hi, end_hi))]
    for lo, hi in windows:
        for timestamp, frame in iter_sequential_frames(
            source, lo, hi, config.refine_interval, roi, source_fps=source_fps
        ):
            scored = score_roi(frame, profile, bank, timestamp=timestamp)
            refined_samples.append(_sample_from_roi_score(scored))
    raw_start, raw_end = refine_from_scores(
        segment.raw_start,
        segment.raw_end,
        refined_samples,
        window,
        lo_bound=lo_bound,
        hi_bound=hi_bound,
    )
    return with_refined_bounds(segment, raw_start, raw_end, config, duration)


def _write_debug(
    debug_dir: Path,
    samples: list[Sample],
    segments: list[ArenaSegment],
    ffmpeg_log: list[str],
    source: Path,
    config: CutterConfig,
) -> None:
    debug_dir.mkdir(parents=True, exist_ok=True)
    with (debug_dir / "samples.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["timestamp", "score", "winning_template", "positive", "borderline", "gladius_present"],
        )
        writer.writeheader()
        for sample in samples:
            writer.writerow(
                {
                    "timestamp": f"{sample.timestamp:.3f}",
                    "score": f"{sample.score:.4f}",
                    "winning_template": sample.winning_template or "",
                    "positive": sample.positive,
                    "borderline": sample.borderline,
                    "gladius_present": sample.gladius_present,
                }
            )
    (debug_dir / "segments.json").write_text(
        json.dumps(
            [
                {
                    "raw_start": seg.raw_start,
                    "raw_end": seg.raw_end,
                    "padded_start": seg.padded_start,
                    "padded_end": seg.padded_end,
                    "confidence": seg.confidence,
                    "merged_gaps": [asdict(gap) for gap in seg.merged_gaps],
                    "warnings": seg.warnings,
                    "truncated_start": seg.truncated_start,
                    "truncated_end": seg.truncated_end,
                }
                for seg in segments
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    (debug_dir / "ffmpeg_commands.txt").write_text("\n".join(ffmpeg_log) + "\n", encoding="utf-8")
    bounds_dir = debug_dir / "boundaries"
    bounds_dir.mkdir(exist_ok=True)
    roi = config.profile.primary_roi
    for index, segment in enumerate(segments, start=1):
        for tag, ts in (("start", segment.raw_start), ("end", segment.raw_end)):
            try:
                frame = extract_frame(source, ts, roi)
            except FfmpegError:
                continue
            cv2.imwrite(str(bounds_dir / f"match_{index:03d}_{tag}.png"), frame)
            mask = text_mask(frame, config.profile.text_hsv)
            cv2.imwrite(str(bounds_dir / f"match_{index:03d}_{tag}_mask.png"), mask)


def run_pipeline(source: Path, output_root: Path, config: CutterConfig) -> Path:
    source = Path(source)
    run_dir = output_run_dir(output_root, source)
    assert_can_write(run_dir, config.overwrite)
    meta = probe(source)
    require_profile(meta.width, meta.height, config.profile)
    bank = TemplateBank.load(config.profile.templates_dir)
    scan_start = 0.0 if config.scan_start is None else max(0.0, config.scan_start)
    scan_end = meta.duration if config.scan_end is None else min(meta.duration, config.scan_end)
    print(
        f"scanning {format_timestamp(scan_start)}-{format_timestamp(scan_end)} "
        f"via {config.scan_backend} every {config.scan_interval}s",
        file=sys.stderr,
    )
    samples: list[Sample] = []
    ffmpeg_log: list[str] = []
    roi = config.profile.primary_roi
    ffmpeg_log.append(
        f"coarse backend={config.scan_backend} {scan_start:.3f}-{scan_end:.3f} "
        f"interval={config.scan_interval} crop={roi.as_ffmpeg_crop()}"
    )
    for timestamp, frame in _iter_coarse(source, scan_start, scan_end, config, meta.fps):
        scored = score_roi(frame, config.profile, bank, timestamp=timestamp)
        samples.append(_sample_from_roi_score(scored))
    print(f"scored {len(samples)} samples", file=sys.stderr)
    segments = segment_samples(samples, config, meta.duration)
    refined: list[ArenaSegment] = []
    for index, segment in enumerate(segments):
        lo_bound = refined[-1].raw_end if refined else None
        hi_bound = segments[index + 1].raw_start if index + 1 < len(segments) else None
        refined.append(
            _refine_segment(
                source,
                segment,
                config,
                bank,
                meta.duration,
                ffmpeg_log,
                meta.fps,
                lo_bound=lo_bound,
                hi_bound=hi_bound,
            )
        )
    review_dir = run_dir / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    sheets: list[str] = []
    run_warnings: list[str] = []
    for index, segment in enumerate(refined, start=1):
        output_name = f"match_{index:03d}.mp4"
        dest = run_dir / output_name
        export_status = "ok"
        export_error = None
        actual_duration = None
        try:
            if config.analysis_ready:
                cmd = analysis_ready_args(
                    source, dest, segment.padded_start, segment.padded_end, config.analysis_crf, config.analysis_fps
                )
                ffmpeg_log.append(" ".join(cmd))
                export_analysis_ready(
                    source,
                    dest,
                    segment.padded_start,
                    segment.padded_end,
                    crf=config.analysis_crf,
                    fps=config.analysis_fps,
                )
            else:
                cmd = stream_copy_args(source, dest, segment.padded_start, segment.padded_end)
                ffmpeg_log.append(" ".join(cmd))
                export_stream_copy(source, dest, segment.padded_start, segment.padded_end)
            actual_duration = verify_clip_decodable(dest)
        except FfmpegError as exc:
            export_status = "error"
            export_error = str(exc)
            run_warnings.append(f"{output_name}: {exc}")
            print(f"export failed {output_name}: {exc}", file=sys.stderr)
        sheet_name = f"match_{index:03d}.jpg"
        sheet_path = review_dir / sheet_name
        try:
            labeled = []
            for ts in contact_sheet_timestamps(segment.padded_start, segment.padded_end):
                frame = extract_frame(source, ts)
                small = cv2.resize(frame, (384, 216), interpolation=cv2.INTER_AREA)
                labeled.append((format_timestamp(ts), small))
            write_contact_sheet(labeled, sheet_path)
        except (FfmpegError, ValueError) as exc:
            run_warnings.append(f"{sheet_name}: {exc}")
            sheet_path.write_bytes(b"")
        records.append(
            match_record(
                match_number=index,
                source_name=source.name,
                output_name=output_name,
                segment=segment,
                profile_name=config.profile.name,
                scan_backend=config.scan_backend,
                export_status=export_status,
                export_error=export_error,
                actual_clip_duration=actual_duration,
            )
        )
        sheets.append(sheet_name)
    run_meta = {
        "source": {
            "path": str(source),
            "filename": source.name,
            "duration": meta.duration,
            "width": meta.width,
            "height": meta.height,
            "fps": meta.fps,
            "video_codec": meta.video_codec,
            "audio_codec": meta.audio_codec,
            "size_bytes": meta.size_bytes,
        },
        "config": {
            "scan_interval": config.scan_interval,
            "entry_window": config.entry_window,
            "entry_positives": config.entry_positives,
            "exit_negatives": config.exit_negatives,
            "merge_gap_seconds": config.merge_gap_seconds,
            "refine_window_seconds": config.refine_window_seconds,
            "refine_interval": config.refine_interval,
            "pre_roll": config.pre_roll,
            "post_roll": config.post_roll,
            "scan_backend": config.scan_backend,
            "analysis_ready": config.analysis_ready,
            "profile": config.profile.name,
            "scan_start": scan_start,
            "scan_end": scan_end,
        },
        "tool_versions": {
            "arena_cutter": __version__,
            "python": sys.version.split()[0],
            "ffmpeg": ffmpeg_version(),
            "ffprobe": ffprobe_version(),
        },
        "benchmark": {
            "window_s": [1200, 1800],
            "interval_s": 2.0,
            "selected_backend": "sequential_ffmpeg",
            "seek_elapsed_s": 74.80,
            "sequential_elapsed_s": 12.04,
            "doc": "docs/benchmark-scan-backends.md",
        },
        "warnings": run_warnings,
    }
    write_manifests(run_dir, records, run_meta)
    (review_dir / "index.html").write_text(render_review_html(records, sheets), encoding="utf-8")
    if config.debug:
        _write_debug(run_dir / "debug", samples, refined, ffmpeg_log, source, config)
    print(f"detected {len(refined)} match(es) -> {run_dir}", file=sys.stderr)
    return run_dir

