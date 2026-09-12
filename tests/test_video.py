from pathlib import Path

import numpy as np

from arena_cutter.video import (
    analysis_ready_args,
    parse_ffprobe_json,
    scheduled_timestamps,
    stream_copy_args,
    write_contact_sheet,
)


def test_scheduled_timestamps_include_start_and_stay_within_end():
    times = scheduled_timestamps(1200, 1800, 2.0)
    assert times[0] == 1200
    assert times[-1] == 1800
    assert all(t <= 1800 for t in times)
    assert times == sorted(times)
    assert len(times) == 301


def test_parse_ffprobe_json_reads_video_stream():
    payload = {
        "streams": [
            {
                "codec_type": "audio",
                "codec_name": "aac",
            },
            {
                "codec_type": "video",
                "codec_name": "h264",
                "width": 1920,
                "height": 1080,
                "r_frame_rate": "60/1",
            },
        ],
        "format": {"duration": "6302.028458", "size": "3331877072"},
    }
    meta = parse_ffprobe_json(payload, Path("vod.mp4"))
    assert meta.width == 1920 and meta.height == 1080
    assert abs(meta.duration - 6302.028458) < 1e-6
    assert meta.fps == 60.0
    assert meta.video_codec == "h264"
    assert meta.audio_codec == "aac"
    assert meta.size_bytes == 3331877072


def test_stream_copy_args_drop_audio_and_copy_video():
    args = stream_copy_args(Path("in.mp4"), Path("out.mp4"), 10.0, 25.0)
    joined = " ".join(args)
    assert "-an" in args
    assert "copy" in args
    assert "10" in joined or "10.0" in joined
    assert "25" in joined or "25.0" in joined


def test_sequential_args_use_select_not_fps_filter():
    from arena_cutter.config import LINGUSTER_1080P
    from arena_cutter.video import sequential_args

    args = sequential_args(Path("in.mp4"), 1200, 1800, 2.0, LINGUSTER_1080P.primary_roi, source_fps=60)
    joined = " ".join(args)
    assert "select=" in joined
    assert "fps=0.5" not in joined
    assert "crop=248:56:916:36" in joined


def test_analysis_ready_args_encode_1080p_30_no_audio():
    args = analysis_ready_args(Path("in.mp4"), Path("out.mp4"), 10.0, 25.0, crf=19, fps=30)
    joined = " ".join(args)
    assert "libx264" in args
    assert "-an" in args
    assert "19" in joined
    assert "30" in joined
    assert "1920" in joined and "1080" in joined


def test_contact_sheet_writes_labeled_image():
    dest = Path(__file__).parent / "_sheet.jpg"
    frames = []
    for i, label in enumerate(["0:00:10.000", "0:00:12.000", "0:00:15.000", "0:00:18.000", "0:00:20.000"]):
        img = np.zeros((40, 60, 3), dtype=np.uint8)
        img[:, :, i % 3] = 200
        frames.append((label, img))
    try:
        write_contact_sheet(frames, dest)
        assert dest.exists() and dest.stat().st_size > 0
    finally:
        if dest.exists():
            dest.unlink()
