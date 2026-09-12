from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from arena_cutter.config import DetectorProfile, HsvRange


class EmptyTemplateBankError(FileNotFoundError):
    """Raised when a detector profile has no binary templates."""


@dataclass(frozen=True)
class FrameScore:
    timestamp: float | None
    primary_score: float
    winning_template: str | None
    is_positive: bool
    is_borderline: bool
    gladius_score: float | None
    gladius_present: bool | None


@dataclass
class TemplateBank:
    templates: list[tuple[str, np.ndarray]]

    @property
    def empty(self) -> bool:
        return not self.templates

    @classmethod
    def load(cls, directory: Path) -> TemplateBank:
        directory = Path(directory)
        loaded: list[tuple[str, np.ndarray]] = []
        if directory.is_dir():
            for path in sorted(directory.glob("*.png")):
                image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
                if image is None:
                    continue
                _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
                loaded.append((path.stem, binary))
        if not loaded:
            raise EmptyTemplateBankError(f"no detector templates in {directory}")
        return cls(templates=loaded)


def text_mask(bgr_roi: np.ndarray, hsv: HsvRange) -> np.ndarray:
    hsv_img = cv2.cvtColor(bgr_roi, cv2.COLOR_BGR2HSV)
    hue, sat, val = cv2.split(hsv_img)
    blue, _green, red = cv2.split(bgr_roi)
    selected = (
        (hue >= hsv.h_min)
        & (hue <= hsv.h_max)
        & (sat >= hsv.s_min)
        & (sat <= hsv.s_max)
        & (val >= hsv.v_min)
        & (val <= hsv.v_max)
        & (blue < hsv.b_max)
        & ((red.astype(np.int16) - blue.astype(np.int16)) > hsv.rb_min)
    )
    mask = (selected.astype(np.uint8)) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1))
    return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


def score_mask(mask: np.ndarray, bank: TemplateBank) -> tuple[float, str | None]:
    if bank.empty:
        raise EmptyTemplateBankError("template bank is empty")
    mask_bool = mask > 0
    mask_on = int(mask_bool.sum())
    best_score = 0.0
    best_name: str | None = None
    for name, template in bank.templates:
        tmpl_bool = template > 0
        if tmpl_bool.shape != mask_bool.shape:
            if (
                tmpl_bool.shape[0] > mask_bool.shape[0]
                or tmpl_bool.shape[1] > mask_bool.shape[1]
            ):
                continue
            score = _best_recall(mask_bool, tmpl_bool)
        else:
            score = _penalized_recall(mask_bool, tmpl_bool, mask_on)
        if score > best_score:
            best_score = score
            best_name = name
    return best_score, best_name


def _penalized_recall(mask_bool: np.ndarray, tmpl_bool: np.ndarray, mask_on: int) -> float:
    template_on = int(tmpl_bool.sum())
    if template_on == 0:
        return 0.0
    hits = int(np.logical_and(mask_bool, tmpl_bool).sum())
    recall = hits / template_on
    ratio = mask_on / template_on
    if ratio > 4.0:
        recall = recall / (1.0 + (ratio - 4.0) / 8.0)
    return float(recall)


def _best_recall(mask_bool: np.ndarray, tmpl_bool: np.ndarray) -> float:
    mask_u8 = (mask_bool.astype(np.uint8)) * 255
    tmpl_u8 = (tmpl_bool.astype(np.uint8)) * 255
    result = cv2.matchTemplate(mask_u8, tmpl_u8, cv2.TM_CCORR_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    x, y = max_loc
    h, w = tmpl_bool.shape
    patch = mask_bool[y : y + h, x : x + w]
    return _penalized_recall(patch, tmpl_bool, int(patch.sum()))


def score_roi(
    bgr_roi: np.ndarray,
    profile: DetectorProfile,
    bank: TemplateBank,
    timestamp: float | None = None,
) -> FrameScore:
    mask = text_mask(bgr_roi, profile.text_hsv)
    score, winner = score_mask(mask, bank)
    return FrameScore(
        timestamp=timestamp,
        primary_score=score,
        winning_template=winner,
        is_positive=score >= profile.positive_threshold,
        is_borderline=(score >= profile.borderline_threshold) and (score < profile.positive_threshold),
        gladius_score=None,
        gladius_present=None,
    )


def score_gladius_roi(bgr_roi: np.ndarray) -> float:
    hsv = cv2.cvtColor(bgr_roi, cv2.COLOR_BGR2HSV)
    green = cv2.inRange(hsv, (40, 80, 80), (85, 255, 255))
    red_a = cv2.inRange(hsv, (0, 80, 80), (10, 255, 255))
    red_b = cv2.inRange(hsv, (170, 80, 80), (180, 255, 255))
    bars = cv2.bitwise_or(green, cv2.bitwise_or(red_a, red_b))
    return float(bars.mean()) / 255.0


def score_frame(
    bgr_full: np.ndarray,
    profile: DetectorProfile,
    bank: TemplateBank,
    timestamp: float | None = None,
    measure_gladius: bool = True,
) -> FrameScore:
    roi = profile.primary_roi.slice(bgr_full)
    scored = score_roi(roi, profile, bank, timestamp=timestamp)
    if not measure_gladius:
        return scored
    gladius = score_gladius_roi(profile.gladius_roi.slice(bgr_full))
    present = gladius >= profile.gladius_threshold
    return FrameScore(
        timestamp=scored.timestamp,
        primary_score=scored.primary_score,
        winning_template=scored.winning_template,
        is_positive=scored.is_positive,
        is_borderline=scored.is_borderline,
        gladius_score=gladius,
        gladius_present=present,
    )
