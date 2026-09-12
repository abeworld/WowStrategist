import csv
import json
from pathlib import Path

from arena_cutter.pipeline import match_record, render_review_html, write_manifests
from arena_cutter.segments import ArenaSegment, GapMerge, format_timestamp


REQUIRED_KEYS = {
    "match_number",
    "source_filename",
    "output_filename",
    "raw_start_s",
    "raw_end_s",
    "padded_start_s",
    "padded_end_s",
    "start_timestamp",
    "end_timestamp",
    "duration_s",
    "actual_clip_duration_s",
    "confidence",
    "mean_score",
    "max_score",
    "primary_positive_count",
    "gladius_positive_count",
    "merged_gaps",
    "truncated_start",
    "truncated_end",
    "detector_profile",
    "scan_backend",
    "export_status",
    "export_error",
    "warnings",
}


def _segment(**kwargs) -> ArenaSegment:
    values = dict(
        raw_start=10.0,
        raw_end=40.0,
        padded_start=0.0,
        padded_end=55.0,
        confidence="high",
        mean_score=0.8,
        max_score=0.95,
        primary_positive_count=12,
        gladius_positive_count=8,
        sample_count=15,
        merged_gaps=[],
        truncated_start=False,
        truncated_end=False,
        warnings=[],
    )
    values.update(kwargs)
    return ArenaSegment(**values)


def test_match_record_has_required_fields_and_timestamps():
    seg = _segment(merged_gaps=[GapMerge(20.0, 28.0, 8.0)], warnings=["merged_gap"])
    record = match_record(
        match_number=1,
        source_name="vod.mp4",
        output_name="match_001.mp4",
        segment=seg,
        profile_name="linguster_1080p",
        scan_backend="sequential_ffmpeg",
        export_status="ok",
        export_error=None,
        actual_clip_duration=56.2,
    )
    assert REQUIRED_KEYS <= set(record)
    assert record["start_timestamp"] == format_timestamp(0.0)
    assert record["end_timestamp"] == format_timestamp(55.0)
    assert record["duration_s"] == 55.0
    assert record["actual_clip_duration_s"] == 56.2
    assert record["merged_gaps"][0]["gap_seconds"] == 8.0


def test_write_manifests_csv_json_and_export_failure_retained():
    ok = match_record(
        1, "vod.mp4", "match_001.mp4", _segment(), "linguster_1080p", "seek", "ok", None, 12.0
    )
    failed = match_record(
        2,
        "vod.mp4",
        "match_002.mp4",
        _segment(raw_start=80, raw_end=100, padded_start=70, padded_end=115),
        "linguster_1080p",
        "seek",
        "error",
        "ffmpeg exited 1",
        None,
    )
    run_meta = {
        "source": {"filename": "vod.mp4", "duration": 200.0},
        "config": {"scan_interval": 2.0},
        "tool_versions": {"python": "3.13"},
        "benchmark": None,
        "warnings": ["match_002 export failed"],
    }
    # Avoid pytest tmp_path on locked Windows temp roots by using a local dir.
    out = Path(__file__).parent / "_manifest_out"
    if out.exists():
        for child in out.iterdir():
            child.unlink()
    else:
        out.mkdir()
    try:
        write_manifests(out, [ok, failed], run_meta)
        csv_rows = list(csv.DictReader((out / "manifest.csv").open(encoding="utf-8")))
        assert len(csv_rows) == 2
        assert csv_rows[1]["export_status"] == "error"
        payload = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
        assert payload["matches"][0]["export_status"] == "ok"
        assert payload["matches"][1]["export_error"] == "ffmpeg exited 1"
        assert payload["source"]["filename"] == "vod.mp4"
        assert payload["warnings"] == ["match_002 export failed"]
    finally:
        for child in out.iterdir():
            child.unlink()
        out.rmdir()


def test_review_html_escapes_and_uses_relative_mp4_links():
    record = match_record(
        1,
        'vod<>&.mp4',
        "match_001.mp4",
        _segment(warnings=["low_confidence"]),
        "linguster_1080p",
        "sequential_ffmpeg",
        "ok",
        None,
        10.0,
    )
    html = render_review_html([record], ["match_001.jpg"])
    assert "<script>" not in html
    assert "vod&lt;&gt;&amp;.mp4" in html
    assert 'href="../match_001.mp4"' in html
    assert "match_001.jpg" in html
    assert "low_confidence" in html
