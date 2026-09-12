from arena_cutter.config import (
    CutterConfig,
    LINGUSTER_1080P,
    UnsupportedProfileError,
    require_profile,
)


def test_profile_is_1080p_with_measured_roi():
    p = LINGUSTER_1080P
    assert p.frame_width == 1920 and p.frame_height == 1080
    assert (p.primary_roi.x, p.primary_roi.y, p.primary_roi.width, p.primary_roi.height) == (
        916,
        36,
        248,
        56,
    )
    assert p.primary_roi.as_ffmpeg_crop() == "248:56:916:36"
    assert p.positive_threshold == 0.28
    assert p.borderline_threshold == 0.18


def test_require_profile_rejects_other_dimensions():
    try:
        require_profile(1280, 720, LINGUSTER_1080P)
    except UnsupportedProfileError as exc:
        message = str(exc)
        assert "1920" in message and "1280" in message
    else:
        raise AssertionError("expected UnsupportedProfileError")


def test_require_profile_accepts_1080p():
    require_profile(1920, 1080, LINGUSTER_1080P)


def test_default_cutter_thresholds():
    c = CutterConfig()
    assert c.scan_interval == 2.0
    assert c.entry_positives == 2 and c.entry_window == 3
    assert c.exit_negatives == 4
    assert c.merge_gap_seconds == 8.0
    assert c.pre_roll == 10.0 and c.post_roll == 15.0
    assert c.refine_window_seconds == 12.0
    assert c.refine_interval == 0.5
