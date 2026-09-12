from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates" / "linguster_1080p"


class UnsupportedProfileError(ValueError):
    """Raised when the source dimensions do not match the V1 detector profile."""


@dataclass(frozen=True)
class Roi:
    x: int
    y: int
    width: int
    height: int

    def as_ffmpeg_crop(self) -> str:
        return f"{self.width}:{self.height}:{self.x}:{self.y}"

    def slice(self, frame: np.ndarray) -> np.ndarray:
        return frame[self.y : self.y + self.height, self.x : self.x + self.width]


@dataclass(frozen=True)
class HsvRange:
    h_min: int
    h_max: int
    s_min: int
    s_max: int
    v_min: int
    v_max: int
    b_max: int
    rb_min: int


@dataclass(frozen=True)
class DetectorProfile:
    name: str
    frame_width: int
    frame_height: int
    primary_roi: Roi
    gladius_roi: Roi
    text_hsv: HsvRange
    positive_threshold: float
    borderline_threshold: float
    gladius_threshold: float
    templates_dir: Path


LINGUSTER_1080P = DetectorProfile(
    name="linguster_1080p",
    frame_width=1920,
    frame_height=1080,
    primary_roi=Roi(x=916, y=36, width=248, height=56),
    gladius_roi=Roi(x=300, y=8, width=240, height=190),
    text_hsv=HsvRange(
        h_min=22,
        h_max=36,
        s_min=70,
        s_max=255,
        v_min=120,
        v_max=255,
        b_max=150,
        rb_min=35,
    ),
    positive_threshold=0.28,
    borderline_threshold=0.18,
    gladius_threshold=0.12,
    templates_dir=TEMPLATES_DIR,
)


@dataclass
class CutterConfig:
    scan_interval: float = 2.0
    entry_window: int = 3
    entry_positives: int = 2
    exit_negatives: int = 4
    merge_gap_seconds: float = 8.0
    refine_window_seconds: float = 12.0
    refine_interval: float = 0.5
    pre_roll: float = 10.0
    post_roll: float = 15.0
    profile: DetectorProfile = field(default_factory=lambda: LINGUSTER_1080P)
    scan_backend: str = "sequential_ffmpeg"
    analysis_ready: bool = False
    debug: bool = False
    overwrite: bool = False
    analysis_crf: int = 19
    analysis_fps: int = 30
    scan_start: float | None = None
    scan_end: float | None = None


def require_profile(width: int, height: int, profile: DetectorProfile) -> None:
    if width != profile.frame_width or height != profile.frame_height:
        raise UnsupportedProfileError(
            f"unsupported layout {width}x{height}; "
            f"profile {profile.name} requires {profile.frame_width}x{profile.frame_height}"
        )
