from __future__ import annotations

import json
import math
import shutil
import subprocess
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import cv2
import numpy as np

from arena_cutter.config import Roi

_CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0


class FfmpegError(RuntimeError):
    """Raised when FFmpeg/ffprobe is missing or a command fails."""


@dataclass(frozen=True)
class VideoMeta:
    path: Path
    duration: float
    width: int
    height: int
    fps: float
    video_codec: str
    audio_codec: str | None
    size_bytes: int


def _run(args: list[str], stdin: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            args,
            input=stdin,
            capture_output=True,
            check=False,
            creationflags=_CREATE_NO_WINDOW,
        )
    except FileNotFoundError as exc:
        raise FfmpegError(f"required executable not found: {args[0]}") from exc


def _check(proc: subprocess.CompletedProcess[bytes], context: str) -> None:
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", errors="replace").strip()
        raise FfmpegError(f"{context} failed ({proc.returncode}): {stderr or 'no stderr'}")


def ffmpeg_bin() -> str:
    found = shutil.which("ffmpeg")
    if not found:
        raise FfmpegError("ffmpeg is not installed or not on PATH")
    return found


def ffprobe_bin() -> str:
    found = shutil.which("ffprobe")
    if not found:
        raise FfmpegError("ffprobe is not installed or not on PATH")
    return found


def ffmpeg_version() -> str:
    proc = _run([ffmpeg_bin(), "-version"])
    _check(proc, "ffmpeg -version")
    return proc.stdout.decode("utf-8", errors="replace").splitlines()[0]


def ffprobe_version() -> str:
    proc = _run([ffprobe_bin(), "-version"])
    _check(proc, "ffprobe -version")
    return proc.stdout.decode("utf-8", errors="replace").splitlines()[0]


def parse_ffprobe_json(payload: dict, path: Path) -> VideoMeta:
    fmt = payload.get("format") or {}
    duration = float(fmt.get("duration") or 0.0)
    try:
        size_bytes = int(fmt.get("size") or 0)
    except (TypeError, ValueError):
        size_bytes = 0
    if size_bytes <= 0 and path.exists():
        size_bytes = path.stat().st_size
    video = None
    audio_codec = None
    for stream in payload.get("streams") or []:
        if stream.get("codec_type") == "video" and video is None:
            video = stream
        elif stream.get("codec_type") == "audio" and audio_codec is None:
            audio_codec = stream.get("codec_name")
    if video is None:
        raise FfmpegError(f"no video stream in {path}")
    rate = str(video.get("avg_frame_rate") or video.get("r_frame_rate") or "0/1")
    fps = _parse_rate(rate)
    return VideoMeta(
        path=Path(path),
        duration=duration,
        width=int(video.get("width") or 0),
        height=int(video.get("height") or 0),
        fps=fps,
        video_codec=str(video.get("codec_name") or "unknown"),
        audio_codec=audio_codec,
        size_bytes=size_bytes,
    )


def _parse_rate(rate: str) -> float:
    if "/" in rate:
        num, den = rate.split("/", 1)
        denominator = float(den)
        if denominator == 0:
            return 0.0
        return float(num) / denominator
    try:
        return float(rate)
    except ValueError:
        return 0.0


def probe(path: Path) -> VideoMeta:
    path = Path(path)
    proc = _run(
        [
            ffprobe_bin(),
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ]
    )
    _check(proc, f"ffprobe {path}")
    payload = json.loads(proc.stdout.decode("utf-8"))
    return parse_ffprobe_json(payload, path)


def scheduled_timestamps(start: float, end: float, interval: float) -> list[float]:
    if interval <= 0:
        raise ValueError("interval must be positive")
    if end < start:
        return []
    count = int(math.floor((end - start) / interval + 1e-9)) + 1
    return [start + i * interval for i in range(count) if start + i * interval <= end + 1e-9]


def stream_copy_args(src: Path, dst: Path, start: float, end: float) -> list[str]:
    return [
        ffmpeg_bin(),
        "-y",
        "-ss",
        f"{start:.3f}",
        "-to",
        f"{end:.3f}",
        "-i",
        str(src),
        "-c:v",
        "copy",
        "-an",
        "-avoid_negative_ts",
        "make_zero",
        str(dst),
    ]


def analysis_ready_args(
    src: Path,
    dst: Path,
    start: float,
    end: float,
    crf: int = 19,
    fps: int = 30,
) -> list[str]:
    return [
        ffmpeg_bin(),
        "-y",
        "-i",
        str(src),
        "-ss",
        f"{start:.3f}",
        "-to",
        f"{end:.3f}",
        "-an",
        "-vf",
        f"scale=1920:1080:flags=bicubic,fps={int(fps)}",
        "-c:v",
        "libx264",
        "-crf",
        str(int(crf)),
        "-preset",
        "veryfast",
        "-pix_fmt",
        "yuv420p",
        str(dst),
    ]


def _crop_filter(roi: Roi | None) -> list[str]:
    if roi is None:
        return []
    return ["-vf", roi.as_ffmpeg_crop() and f"crop={roi.as_ffmpeg_crop()}"]


def _select_skip(source_fps: float, interval: float) -> int:
    return max(1, int(round(source_fps * interval)))


def sequential_args(
    src: Path,
    start: float,
    end: float,
    interval: float,
    roi: Roi,
    source_fps: float = 60.0,
) -> list[str]:
    # Pad by one interval so the last scheduled timestamp is included.
    duration = max(0.0, end - start + interval)
    skip = _select_skip(source_fps, interval)
    return [
        ffmpeg_bin(),
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        f"{start:.3f}",
        "-t",
        f"{duration:.3f}",
        "-i",
        str(src),
        "-vf",
        f"crop={roi.as_ffmpeg_crop()},select=not(mod(n\\,{skip}))",
        "-vsync",
        "0",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "bgr24",
        "pipe:1",
    ]


def seek_frame_args(src: Path, timestamp: float, roi: Roi | None) -> list[str]:
    args = [
        ffmpeg_bin(),
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        f"{timestamp:.3f}",
        "-i",
        str(src),
        "-frames:v",
        "1",
    ]
    args.extend(_crop_filter(roi))
    args.extend(["-f", "rawvideo", "-pix_fmt", "bgr24", "pipe:1"])
    return args


def iter_sequential_frames(
    path: Path,
    start: float,
    end: float,
    interval: float,
    roi: Roi,
    source_fps: float = 60.0,
) -> Iterator[tuple[float, np.ndarray]]:
    args = sequential_args(path, start, end, interval, roi, source_fps=source_fps)
    frame_bytes = roi.width * roi.height * 3
    proc = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=_CREATE_NO_WINDOW,
    )
    assert proc.stdout is not None
    stderr_chunks: list[bytes] = []

    def _drain_stderr() -> None:
        if proc.stderr is not None:
            stderr_chunks.append(proc.stderr.read())

    drainer = threading.Thread(target=_drain_stderr, daemon=True)
    drainer.start()
    index = 0
    try:
        while True:
            buf = proc.stdout.read(frame_bytes)
            if not buf:
                break
            if len(buf) < frame_bytes:
                break
            frame = np.frombuffer(buf, dtype=np.uint8).reshape((roi.height, roi.width, 3)).copy()
            timestamp = start + index * interval
            if timestamp > end + 1e-6:
                break
            yield (timestamp, frame)
            index += 1
    finally:
        proc.stdout.close()
        proc.wait()
        drainer.join(timeout=5)
        stderr = b"".join(stderr_chunks)
        if proc.returncode not in (0, None) and index == 0:
            raise FfmpegError(
                f"sequential scan failed ({proc.returncode}): "
                f"{stderr.decode('utf-8', errors='replace')}"
            )


def iter_seek_frames(
    path: Path,
    start: float,
    end: float,
    interval: float,
    roi: Roi | None,
) -> Iterator[tuple[float, np.ndarray]]:
    for timestamp in scheduled_timestamps(start, end, interval):
        args = seek_frame_args(path, timestamp, roi)
        proc = _run(args)
        if proc.returncode != 0 or not proc.stdout:
            continue
        raw = proc.stdout
        if roi is None:
            raise FfmpegError("seek backend requires an ROI for raw frame reshape")
        expected = roi.width * roi.height * 3
        if len(raw) < expected:
            continue
        frame = np.frombuffer(raw[:expected], dtype=np.uint8).reshape((roi.height, roi.width, 3)).copy()
        yield timestamp, frame


def extract_frame(path: Path, timestamp: float, roi: Roi | None = None) -> np.ndarray:
    args = [
        ffmpeg_bin(),
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        f"{timestamp:.3f}",
        "-i",
        str(path),
        "-frames:v",
        "1",
    ]
    if roi is not None:
        args.extend(["-vf", f"crop={roi.as_ffmpeg_crop()}"])
    args.extend(["-f", "image2pipe", "-vcodec", "png", "pipe:1"])
    proc = _run(args)
    _check(proc, f"extract frame at {timestamp:.3f}")
    array = np.frombuffer(proc.stdout, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise FfmpegError(f"could not decode frame at {timestamp:.3f}s")
    return image


def export_stream_copy(src: Path, dst: Path, start: float, end: float) -> None:
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    proc = _run(stream_copy_args(src, dst, start, end))
    _check(proc, f"stream-copy {dst.name}")


def export_analysis_ready(
    src: Path,
    dst: Path,
    start: float,
    end: float,
    crf: int = 19,
    fps: int = 30,
) -> None:
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    proc = _run(analysis_ready_args(src, dst, start, end, crf=crf, fps=fps))
    _check(proc, f"analysis-ready {dst.name}")


def verify_clip_decodable(path: Path) -> float:
    meta = probe(path)
    if meta.duration <= 0 or meta.width <= 0:
        raise FfmpegError(f"exported clip is not decodable: {path}")
    extract_frame(path, 0.0)
    return meta.duration


def write_contact_sheet(labeled_bgr_frames: list[tuple[str, np.ndarray]], dest: Path) -> None:
    if not labeled_bgr_frames:
        raise ValueError("contact sheet requires at least one frame")
    tiles = []
    height = max(frame.shape[0] for _, frame in labeled_bgr_frames)
    width = max(frame.shape[1] for _, frame in labeled_bgr_frames)
    banner = 28
    for label, frame in labeled_bgr_frames:
        tile = np.zeros((height + banner, width, 3), dtype=np.uint8)
        resized = frame
        if frame.shape[0] != height or frame.shape[1] != width:
            resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
        tile[banner : banner + height, :width] = resized
        cv2.putText(
            tile,
            label,
            (8, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (240, 240, 240),
            1,
            cv2.LINE_AA,
        )
        tiles.append(tile)
    sheet = np.concatenate(tiles, axis=1)
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(dest), sheet):
        raise FfmpegError(f"failed to write contact sheet {dest}")
