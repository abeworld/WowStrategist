from __future__ import annotations

import re
from dataclasses import dataclass, field

from arena_cutter.config import CutterConfig


@dataclass(frozen=True)
class Sample:
    timestamp: float
    positive: bool
    borderline: bool
    score: float
    winning_template: str | None
    gladius_present: bool | None


@dataclass(frozen=True)
class GapMerge:
    gap_start: float
    gap_end: float
    gap_seconds: float


@dataclass
class ArenaSegment:
    raw_start: float
    raw_end: float
    padded_start: float
    padded_end: float
    confidence: str
    mean_score: float
    max_score: float
    primary_positive_count: int
    gladius_positive_count: int
    sample_count: int
    merged_gaps: list[GapMerge] = field(default_factory=list)
    truncated_start: bool = False
    truncated_end: bool = False
    warnings: list[str] = field(default_factory=list)


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def format_timestamp(seconds: float) -> str:
    if seconds < 0:
        seconds = 0.0
    total_ms = int(round(seconds * 1000.0))
    hours, rem_ms = divmod(total_ms, 3_600_000)
    minutes, rem_ms = divmod(rem_ms, 60_000)
    secs, ms = divmod(rem_ms, 1000)
    return f"{hours}:{minutes:02d}:{secs:02d}.{ms:03d}"


def sanitize_video_name(name: str) -> str:
    stem = name
    if stem.lower().endswith(".mp4"):
        stem = stem[:-4]
    cleaned = re.sub(r"[^A-Za-z0-9._+-]+", "_", stem).strip("._")
    return cleaned or "vod"


def contact_sheet_timestamps(start: float, end: float, count: int = 5) -> list[float]:
    if count <= 1:
        return [start]
    if end < start:
        end = start
    if end == start:
        return [start] * count
    fractions = [0.0, 0.2, 0.5, 0.8, 1.0]
    if count != 5:
        fractions = [i / (count - 1) for i in range(count)]
    times = [start + (end - start) * f for f in fractions]
    return [clamp(t, start, end) for t in times]


def segment_samples(
    samples: list[Sample],
    config: CutterConfig,
    duration: float,
) -> list[ArenaSegment]:
    if not samples:
        return []
    ordered = sorted(samples, key=lambda s: s.timestamp)
    raw_spans = _raw_spans(ordered, config)
    merged = _merge_spans(raw_spans, config.merge_gap_seconds)
    return [_finalize(span, config, duration) for span in merged]


@dataclass
class _Span:
    start: float
    end: float
    members: list[Sample]
    truncated_start: bool = False
    truncated_end: bool = False
    merged_gaps: list[GapMerge] = field(default_factory=list)


def _raw_spans(samples: list[Sample], config: CutterConfig) -> list[_Span]:
    spans: list[_Span] = []
    state = "OUTSIDE"
    current: _Span | None = None
    neg_run = 0

    for index, sample in enumerate(samples):
        if state == "OUTSIDE":
            window_start = max(0, index - config.entry_window + 1)
            window = samples[window_start : index + 1]
            if sum(1 for item in window if item.positive) >= config.entry_positives:
                first_positive = next(item for item in window if item.positive)
                start_time = first_positive.timestamp
                first_pos_index = next(
                    i for i, item in enumerate(samples) if item is first_positive or (
                        item.timestamp == first_positive.timestamp and item.positive
                    )
                )
                if first_pos_index > 0 and samples[first_pos_index - 1].borderline:
                    start_time = samples[first_pos_index - 1].timestamp
                members = [
                    item
                    for item in samples
                    if start_time <= item.timestamp <= sample.timestamp
                    and (item.positive or item.borderline)
                ]
                last_active = max(
                    (item.timestamp for item in members),
                    default=sample.timestamp,
                )
                current = _Span(
                    start=start_time,
                    end=last_active,
                    members=members,
                    truncated_start=start_time <= samples[0].timestamp + 1e-9
                    and samples[0].timestamp <= 1e-9,
                )
                state = "ARENA"
                neg_run = 0
            continue

        assert current is not None
        if sample.positive or sample.borderline:
            current.end = sample.timestamp
            current.members.append(sample)
            neg_run = 0
            state = "ARENA"
            continue

        if state == "ARENA":
            state = "EXIT_CANDIDATE"
            neg_run = 1
        else:
            neg_run += 1

        if neg_run >= config.exit_negatives:
            spans.append(current)
            current = None
            state = "OUTSIDE"
            neg_run = 0

    if current is not None:
        current.truncated_end = True
        spans.append(current)
    return spans


def _merge_spans(spans: list[_Span], merge_gap: float) -> list[_Span]:
    if not spans:
        return []
    merged = [spans[0]]
    for span in spans[1:]:
        prev = merged[-1]
        gap = span.start - prev.end
        if gap <= merge_gap:
            prev.merged_gaps.append(
                GapMerge(gap_start=prev.end, gap_end=span.start, gap_seconds=gap)
            )
            prev.end = span.end
            prev.members.extend(span.members)
            prev.truncated_end = span.truncated_end
            prev.merged_gaps.extend(span.merged_gaps)
        else:
            merged.append(span)
    return merged


def _finalize(span: _Span, config: CutterConfig, duration: float) -> ArenaSegment:
    positives = [s for s in span.members if s.positive]
    active = [s for s in span.members if s.positive or s.borderline]
    scores = [s.score for s in active] or [0.0]
    mean_score = sum(scores) / len(scores)
    max_score = max(scores)
    gladius_count = sum(1 for s in span.members if s.gladius_present)
    confidence = _confidence(mean_score, len(positives), gladius_count)
    warnings: list[str] = []
    if confidence == "low":
        warnings.append("low_confidence")
    if span.truncated_start:
        warnings.append("truncated_start")
    if span.truncated_end:
        warnings.append("truncated_end")
    if span.merged_gaps:
        warnings.append("merged_gap")
    padded_start = clamp(span.start - config.pre_roll, 0.0, duration)
    padded_end = clamp(span.end + config.post_roll, 0.0, duration)
    if padded_end < padded_start:
        padded_end = padded_start
    return ArenaSegment(
        raw_start=span.start,
        raw_end=span.end,
        padded_start=padded_start,
        padded_end=padded_end,
        confidence=confidence,
        mean_score=mean_score,
        max_score=max_score,
        primary_positive_count=len(positives),
        gladius_positive_count=gladius_count,
        sample_count=len(span.members),
        merged_gaps=list(span.merged_gaps),
        truncated_start=span.truncated_start,
        truncated_end=span.truncated_end,
        warnings=warnings,
    )


def _confidence(mean_score: float, positive_count: int, gladius_count: int) -> str:
    if mean_score >= 0.6 and positive_count >= 5:
        return "high"
    if mean_score >= 0.4 or gladius_count >= 3:
        return "medium"
    return "low"
