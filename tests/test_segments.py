from arena_cutter.config import CutterConfig
from arena_cutter.segments import (
    Sample,
    clamp,
    contact_sheet_timestamps,
    format_timestamp,
    sanitize_video_name,
    segment_samples,
)


def test_format_timestamp():
    assert format_timestamp(0) == "0:00:00.000"
    assert format_timestamp(1336.0) == "0:22:16.000"
    assert format_timestamp(3600 + 5.25) == "1:00:05.250"


def test_contact_sheet_positions_and_short_clip():
    ts = contact_sheet_timestamps(100, 200, 5)
    assert ts[0] == 100 and ts[-1] == 200
    assert ts == sorted(ts)
    assert len(ts) == 5
    short = contact_sheet_timestamps(5, 6, 5)
    assert short[0] == 5 and short[-1] == 6
    assert len(short) == 5


def test_clamp_and_sanitize():
    assert clamp(-1, 0, 10) == 0
    assert clamp(11, 0, 10) == 10
    assert clamp(5, 0, 10) == 5
    name = sanitize_video_name("2v2 SPR +2200.mp4")
    assert name
    assert "/" not in sanitize_video_name("a/b\\c")
    assert "\\" not in sanitize_video_name("a/b\\c")


def _samples(times_and_flags):
    out = []
    for item in times_and_flags:
        t, flag = item[0], item[1]
        score = item[2] if len(item) > 2 else None
        positive = flag == "pos"
        borderline = flag == "bord"
        if score is None:
            score = 0.9 if positive else (0.22 if borderline else 0.0)
        out.append(
            Sample(
                timestamp=t,
                positive=positive,
                borderline=borderline,
                score=score,
                winning_template="gold_green_22" if positive else None,
                gladius_present=None,
            )
        )
    return out


def test_entry_requires_two_of_three_positives():
    cfg = CutterConfig()
    samples = _samples(
        [
            (0, "neg"),
            (2, "pos"),
            (4, "neg"),
            (6, "pos"),
            (8, "pos"),
            (10, "pos"),
            (12, "pos"),
            (14, "neg"),
            (16, "neg"),
            (18, "neg"),
            (20, "neg"),
        ]
    )
    segs = segment_samples(samples, cfg, duration=30)
    assert len(segs) == 1
    # 2-of-3 at t=2,4,6 is pos/neg/pos; recall-first start is the earliest positive.
    assert segs[0].raw_start == 2
    assert segs[0].raw_end == 12


def test_isolated_weak_spike_is_ignored():
    cfg = CutterConfig()
    samples = _samples(
        [
            (0, "neg"),
            (2, "pos"),
            (4, "neg"),
            (6, "neg"),
            (8, "neg"),
            (10, "neg"),
        ]
    )
    assert segment_samples(samples, cfg, duration=20) == []


def test_exit_requires_four_consecutive_negatives():
    cfg = CutterConfig()
    samples = _samples(
        [
            (0, "pos"),
            (2, "pos"),
            (4, "pos"),
            (6, "neg"),
            (8, "neg"),
            (10, "pos"),
            (12, "pos"),
            (14, "neg"),
            (16, "neg"),
            (18, "neg"),
            (20, "neg"),
        ]
    )
    segs = segment_samples(samples, cfg, duration=40)
    assert len(segs) == 1
    assert segs[0].raw_start == 0
    assert segs[0].raw_end == 12


def test_temporary_disappearance_does_not_split():
    cfg = CutterConfig()
    samples = _samples(
        [(t, "pos") for t in range(0, 10, 2)]
        + [(10, "neg"), (12, "neg"), (14, "pos"), (16, "pos")]
        + [(t, "neg") for t in range(18, 26, 2)]
    )
    segs = segment_samples(samples, cfg, duration=40)
    assert len(segs) == 1
    assert segs[0].raw_end == 16


def test_short_gap_merges_and_16s_gap_does_not():
    cfg = CutterConfig()
    first = _samples(
        [(t, "pos") for t in (0, 2, 4)] + [(t, "neg") for t in (6, 8, 10, 12)]
    )
    second_merged = _samples(
        [(t, "pos") for t in (20, 22, 24)] + [(t, "neg") for t in (26, 28, 30, 32)]
    )
    # gap from raw_end=4 to next raw_start=20 is 16s — must not merge
    segs = segment_samples(first + second_merged, cfg, duration=50)
    assert len(segs) == 2

    close_second = _samples(
        [(t, "pos") for t in (12, 14, 16)] + [(t, "neg") for t in (18, 20, 22, 24)]
    )
    # first raw_end=4, second raw_start=12, gap=8s — merge at the 8s default
    merged = segment_samples(first + close_second, cfg, duration=40)
    assert len(merged) == 1
    assert merged[0].raw_start == 0
    assert merged[0].raw_end == 16
    assert merged[0].merged_gaps
    assert merged[0].merged_gaps[0].gap_seconds == 8

    ten = _samples(
        [(t, "pos") for t in (16, 18, 20)] + [(t, "neg") for t in (22, 24, 26, 28)]
    )
    # first raw_end=4, this block starts at 16, gap=12s — must not merge at 8s default
    split_twelve = segment_samples(first + ten, cfg, duration=40)
    assert len(split_twelve) == 2


def test_padding_applied_after_segmentation_and_clamped():
    cfg = CutterConfig()
    samples = _samples(
        [(t, "pos") for t in (2, 4, 6)] + [(t, "neg") for t in (8, 10, 12, 14)]
    )
    segs = segment_samples(samples, cfg, duration=20)
    assert len(segs) == 1
    assert segs[0].raw_start == 2
    assert segs[0].raw_end == 6
    assert segs[0].padded_start == 0  # 2-10 clamped
    assert segs[0].padded_end == 20  # 6+15=21 clamped to 20


def test_borderline_expands_start_earlier_and_end_later():
    cfg = CutterConfig()
    samples = _samples(
        [
            (0, "neg"),
            (2, "bord"),
            (4, "pos"),
            (6, "pos"),
            (8, "pos"),
            (10, "bord"),
            (12, "neg"),
            (14, "neg"),
            (16, "neg"),
            (18, "neg"),
        ]
    )
    segs = segment_samples(samples, cfg, duration=30)
    assert len(segs) == 1
    assert segs[0].raw_start == 2
    assert segs[0].raw_end == 10


def test_vod_start_and_end_in_arena_are_kept_and_flagged():
    cfg = CutterConfig()
    samples = _samples([(t, "pos") for t in range(0, 10, 2)])
    segs = segment_samples(samples, cfg, duration=8)
    assert len(segs) == 1
    assert segs[0].truncated_start is True
    assert segs[0].truncated_end is True
    assert segs[0].raw_start == 0
    assert segs[0].raw_end == 8


def test_low_confidence_persistent_segment_is_retained():
    cfg = CutterConfig()
    samples = _samples(
        [(t, "pos", 0.30) for t in (0, 2, 4, 6)]
        + [(t, "neg", 0.0) for t in (8, 10, 12, 14)]
    )
    segs = segment_samples(samples, cfg, duration=30)
    assert len(segs) == 1
    assert segs[0].confidence == "low"
    assert "low_confidence" in segs[0].warnings


def test_very_short_game_is_kept():
    cfg = CutterConfig()
    samples = _samples(
        [(0, "pos"), (2, "pos")] + [(t, "neg") for t in (4, 6, 8, 10)]
    )
    segs = segment_samples(samples, cfg, duration=20)
    assert len(segs) == 1
    assert segs[0].raw_end - segs[0].raw_start == 2
