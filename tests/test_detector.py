from pathlib import Path

import cv2
import pytest

from arena_cutter.config import LINGUSTER_1080P
from arena_cutter.detector import (
    EmptyTemplateBankError,
    TemplateBank,
    score_frame,
    score_roi,
)

FIX = Path(__file__).parent / "fixtures" / "roi"


@pytest.fixture(scope="module")
def bank() -> TemplateBank:
    return TemplateBank.load(LINGUSTER_1080P.templates_dir)


def score_file(name: str, bank: TemplateBank):
    img = cv2.imread(str(FIX / name))
    assert img is not None, name
    return score_roi(img, LINGUSTER_1080P, bank)


def test_positive_fixtures_are_arena(bank):
    for name in [
        "positive_gold_green.png",
        "positive_gold_green_dark.png",
        "positive_green_gold.png",
        "ending_zero.png",
        "count_one.png",
    ]:
        result = score_file(name, bank)
        assert result.is_positive, (name, result.primary_score, result.winning_template)
        assert result.winning_template


def test_obscured_count_change_still_positive(bank):
    result = score_file("obscured_count_one.png", bank)
    assert result.is_positive, (result.primary_score, result.winning_template)


def test_outside_and_loading_are_not_positive(bank):
    for name in [
        "outside_world.png",
        "outside_buildings.png",
        "outside_start.png",
        "loading.png",
    ]:
        result = score_file(name, bank)
        assert not result.is_positive, (name, result.primary_score)


def test_empty_bank_raises():
    with pytest.raises(EmptyTemplateBankError):
        TemplateBank.load(FIX / "does_not_exist_templates")


def test_score_frame_without_gladius_leaves_gladius_unmeasured(bank):
    img = cv2.imread(str(FIX / "positive_gold_green.png"))
    # ROI-sized image: measuring Gladius would be invalid; caller must pass full frame.
    result = score_roi(img, LINGUSTER_1080P, bank)
    assert result.gladius_score is None
    assert result.gladius_present is None


def test_score_frame_gladius_none_when_disabled(bank):
    full = cv2.imread(str(FIX / "positive_gold_green.png"))
    # Pad into a fake 1920x1080 so the primary ROI can be sliced.
    import numpy as np

    frame = np.zeros((1080, 1920, 3), dtype=full.dtype)
    roi = LINGUSTER_1080P.primary_roi
    frame[roi.y : roi.y + roi.height, roi.x : roi.x + roi.width] = full
    result = score_frame(frame, LINGUSTER_1080P, bank, timestamp=1.0, measure_gladius=False)
    assert result.is_positive
    assert result.gladius_score is None
    assert result.timestamp == 1.0
