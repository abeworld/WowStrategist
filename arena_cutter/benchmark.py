from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from arena_cutter.config import LINGUSTER_1080P
from arena_cutter.detector import TemplateBank, score_roi
from arena_cutter.segments import format_timestamp
from arena_cutter.video import iter_seek_frames, iter_sequential_frames, probe, scheduled_timestamps


@dataclass
class BackendResult:
    name: str
    elapsed_s: float
    sample_count: int
    first_timestamp: float | None
    last_timestamp: float | None
    positive_count: int
    timestamps: list[float]
    positives: list[bool]
    scores: list[float]


def _scan(name: str, source: Path, start: float, end: float, interval: float, fps: float) -> BackendResult:
    roi = LINGUSTER_1080P.primary_roi
    bank = TemplateBank.load(LINGUSTER_1080P.templates_dir)
    iterator = (
        iter_seek_frames(source, start, end, interval, roi)
        if name == "seek"
        else iter_sequential_frames(source, start, end, interval, roi, source_fps=fps)
    )
    t0 = time.perf_counter()
    timestamps: list[float] = []
    positives: list[bool] = []
    scores: list[float] = []
    for ts, frame in iterator:
        scored = score_roi(frame, LINGUSTER_1080P, bank, timestamp=ts)
        timestamps.append(ts)
        positives.append(scored.is_positive)
        scores.append(scored.primary_score)
    elapsed = time.perf_counter() - t0
    return BackendResult(
        name=name,
        elapsed_s=elapsed,
        sample_count=len(timestamps),
        first_timestamp=timestamps[0] if timestamps else None,
        last_timestamp=timestamps[-1] if timestamps else None,
        positive_count=sum(1 for flag in positives if flag),
        timestamps=timestamps,
        positives=positives,
        scores=scores,
    )


def _timestamp_errors(result: BackendResult, start: float, end: float, interval: float) -> dict:
    expected = scheduled_timestamps(start, end, interval)
    if not result.timestamps:
        return {"ok": False, "reason": "no samples"}
    monotonic = all(
        result.timestamps[i] <= result.timestamps[i + 1] for i in range(len(result.timestamps) - 1)
    )
    mapped = []
    for ts in result.timestamps:
        nearest = min(expected, key=lambda exp: abs(exp - ts))
        mapped.append(abs(nearest - ts))
    max_err = max(mapped) if mapped else None
    return {
        "ok": monotonic and result.sample_count == len(expected) and (max_err or 0) <= interval * 0.5,
        "monotonic": monotonic,
        "expected_count": len(expected),
        "actual_count": result.sample_count,
        "max_abs_error_s": max_err,
        "tolerance_s": interval * 0.5,
    }


def choose_backend(seek: BackendResult, sequential: BackendResult, seek_ok: bool, seq_ok: bool) -> str:
    if seq_ok and not seek_ok:
        return "sequential_ffmpeg"
    if seek_ok and not seq_ok:
        return "seek"
    if not seq_ok and not seek_ok:
        return "sequential_ffmpeg"
    if abs(seek.elapsed_s - sequential.elapsed_s) / max(seek.elapsed_s, sequential.elapsed_s, 1e-6) <= 0.20:
        return "sequential_ffmpeg"
    return "sequential_ffmpeg" if sequential.elapsed_s <= seek.elapsed_s else "seek"


def render_markdown(
    source: Path,
    start: float,
    end: float,
    interval: float,
    seek: BackendResult,
    sequential: BackendResult,
    winner: str,
) -> str:
    seek_ts = _timestamp_errors(seek, start, end, interval)
    seq_ts = _timestamp_errors(sequential, start, end, interval)
    n = min(len(seek.positives), len(sequential.positives))
    diffs = [
        i
        for i in range(n)
        if seek.positives[i] != sequential.positives[i]
        and abs(seek.timestamps[i] - sequential.timestamps[i]) <= interval * 0.5
    ]
    checkpoints = []
    for label, ts in [("arena ~20:00", 1200), ("world ~20:50", 1250), ("result ~22:14", 1334), ("world ~22:16", 1336), ("prep ~22:32", 1352)]:
        checkpoints.append(_checkpoint_line(label, ts, seek, sequential, interval))
    return f"""# Scan backend benchmark

Source: `{source.name}`
Window: {format_timestamp(start)} – {format_timestamp(end)} ({start:.0f}–{end:.0f}s)
Interval: {interval}s

## Timing

| Backend | Elapsed (s) | Samples | Positives | First ts | Last ts |
| --- | ---: | ---: | ---: | ---: | ---: |
| seek | {seek.elapsed_s:.2f} | {seek.sample_count} | {seek.positive_count} | {seek.first_timestamp} | {seek.last_timestamp} |
| sequential_ffmpeg | {sequential.elapsed_s:.2f} | {sequential.sample_count} | {sequential.positive_count} | {sequential.first_timestamp} | {sequential.last_timestamp} |

## Timestamp reliability

| Backend | OK | Monotonic | Expected count | Max abs error (s) | Tolerance (s) |
| --- | --- | --- | ---: | ---: | ---: |
| seek | {seek_ts['ok']} | {seek_ts.get('monotonic')} | {seek_ts.get('expected_count')} | {seek_ts.get('max_abs_error_s')} | {seek_ts.get('tolerance_s')} |
| sequential_ffmpeg | {seq_ts['ok']} | {seq_ts.get('monotonic')} | {seq_ts.get('expected_count')} | {seq_ts.get('max_abs_error_s')} | {seq_ts.get('tolerance_s')} |

Classification disagreements (aligned timestamps): {len(diffs)}

## Known-event checkpoints

{chr(10).join(checkpoints)}

## Choice

Selected backend: **{winner}**

Rule: faster reliable method; if elapsed times differ by no more than 20%, prefer sequential FFmpeg.
"""


def _checkpoint_line(label: str, ts: float, seek: BackendResult, sequential: BackendResult, interval: float) -> str:
    def nearest(result: BackendResult) -> str:
        if not result.timestamps:
            return "missing"
        idx = min(range(len(result.timestamps)), key=lambda i: abs(result.timestamps[i] - ts))
        got = result.timestamps[idx]
        if abs(got - ts) > interval:
            return f"no sample near {ts}"
        flag = "positive" if result.positives[idx] else "negative"
        return f"{got:.1f}s {flag} score={result.scores[idx]:.3f}"

    return f"- {label}: seek={nearest(seek)}; sequential={nearest(sequential)}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="arena_cutter.benchmark")
    parser.add_argument("source")
    parser.add_argument("--start", type=float, default=1200.0)
    parser.add_argument("--end", type=float, default=1800.0)
    parser.add_argument("--interval", type=float, default=2.0)
    parser.add_argument("--output", default="docs/benchmark-scan-backends.md")
    args = parser.parse_args(argv)
    source = Path(args.source)
    meta = probe(source)
    print(f"benchmark {source.name} {args.start}-{args.end}s", file=sys.stderr)
    print("running seek...", file=sys.stderr)
    seek = _scan("seek", source, args.start, args.end, args.interval, meta.fps)
    print(f"seek {seek.elapsed_s:.1f}s n={seek.sample_count}", file=sys.stderr)
    print("running sequential...", file=sys.stderr)
    sequential = _scan("sequential_ffmpeg", source, args.start, args.end, args.interval, meta.fps)
    print(f"sequential {sequential.elapsed_s:.1f}s n={sequential.sample_count}", file=sys.stderr)
    seek_ok = bool(_timestamp_errors(seek, args.start, args.end, args.interval)["ok"])
    seq_ok = bool(_timestamp_errors(sequential, args.start, args.end, args.interval)["ok"])
    winner = choose_backend(seek, sequential, seek_ok, seq_ok)
    markdown = render_markdown(source, args.start, args.end, args.interval, seek, sequential, winner)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown, encoding="utf-8")
    summary = {
        "winner": winner,
        "seek": {k: getattr(seek, k) for k in ("name", "elapsed_s", "sample_count", "positive_count", "first_timestamp", "last_timestamp")},
        "sequential_ffmpeg": {k: getattr(sequential, k) for k in ("name", "elapsed_s", "sample_count", "positive_count", "first_timestamp", "last_timestamp")},
    }
    print(json.dumps(summary, indent=2))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
