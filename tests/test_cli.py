from pathlib import Path

import pytest

from arena_cutter.__main__ import parse_args
from arena_cutter.pipeline import OutputExistsError, assert_can_write, output_run_dir
from arena_cutter.segments import Sample, sanitize_video_name
from arena_cutter.pipeline import refine_from_scores


def test_parse_args_required_flags():
    ns = parse_args(
        [
            "vod.mp4",
            "--output",
            "out",
            "--debug",
            "--analysis-ready",
            "--scan-interval",
            "1.5",
            "--pre-roll",
            "8",
            "--post-roll",
            "12",
            "--overwrite",
        ]
    )
    assert ns.source == "vod.mp4"
    assert ns.output == "out"
    assert ns.debug is True
    assert ns.analysis_ready is True
    assert ns.scan_interval == 1.5
    assert ns.pre_roll == 8.0
    assert ns.post_roll == 12.0
    assert ns.overwrite is True


def test_overwrite_guard_blocks_existing_artifacts():
    run_dir = Path(__file__).parent / "_overwrite_dir"
    run_dir.mkdir(exist_ok=True)
    artifact = run_dir / "manifest.json"
    artifact.write_text("{}", encoding="utf-8")
    try:
        with pytest.raises(OutputExistsError):
            assert_can_write(run_dir, overwrite=False)
        assert_can_write(run_dir, overwrite=True)
    finally:
        artifact.unlink()
        run_dir.rmdir()


def test_output_run_dir_uses_sanitized_name():
    path = output_run_dir(Path("output"), Path("2v2 SPR +2200.mp4"))
    assert path.name == sanitize_video_name("2v2 SPR +2200.mp4")


def test_refine_picks_earlier_start_and_later_end():
    samples = [
        Sample(8.0, False, True, 0.22, None, None),
        Sample(8.5, True, False, 0.9, "gold_green_22", None),
        Sample(10.0, True, False, 0.9, "gold_green_22", None),
        Sample(40.0, True, False, 0.9, "gold_green_22", None),
        Sample(41.0, True, False, 0.5, "gold_green_22", None),
        Sample(41.5, False, True, 0.2, None, None),
        Sample(42.0, False, False, 0.0, None, None),
    ]
    start, end = refine_from_scores(10.0, 40.0, samples, window=12.0)
    assert start == 8.0
    assert end == 41.5


def test_refine_does_not_consume_neighbor_match():
    samples = [
        Sample(90.0, True, False, 0.9, "gold_green_22", None),
        Sample(100.0, True, False, 0.9, "gold_green_22", None),
        Sample(104.0, False, False, 0.0, None, None),
        Sample(110.0, True, False, 0.9, "gold_green_22", None),
        Sample(120.0, True, False, 0.9, "gold_green_22", None),
    ]
    start, end = refine_from_scores(100.0, 100.0, samples, window=12.0, hi_bound=110.0)
    assert end < 110.0
    start2, end2 = refine_from_scores(110.0, 120.0, samples, window=12.0, lo_bound=end)
    assert start2 >= end
