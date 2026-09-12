# WoW Arena Auto-Cutter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local Python CLI that takes one 1920×1080 Linguster Warmane arena VOD, detects each arena session from the top-center Gold/Green team-status block, exports one MP4 per match with manifests and a static review page.

**Architecture:** A 1080p detector profile color-masks the fixed team-status ROI and scores binary templates by penalized recall. A persistence state machine (`OUTSIDE → CANDIDATE → ARENA → EXIT_CANDIDATE → OUTSIDE`) turns per-sample scores into padded segments. FFmpeg scan backends, export, and review artifacts are orchestrated by `pipeline.py` behind `python -m arena_cutter`.

**Tech Stack:** Python 3.13+ (venv), OpenCV, NumPy, pytest, system FFmpeg/ffprobe. Standard library for argparse, csv, json, html, subprocess.

**Spec:** `docs/superpowers/specs/2026-09-04-wow-arena-auto-cutter-design.md`

## Global Constraints

- Python + OpenCV + NumPy + FFmpeg/ffprobe only; no OCR, cloud APIs, LLMs, neural models, or extra frameworks.
- V1 supports only 1920×1080; other dimensions raise an explicit unsupported-profile error (no silent resize).
- Primary detector is the Gold/Green team-status block, not Gladius and not Shadow Sight.
- Gladius is secondary corroboration only; its absence must not block preparation or export.
- Recall over precision: earlier start, later end, merge short gaps, never silently drop plausible segments.
- Initial thresholds: scan 2s, entry 2/3 positives, exit 4 consecutive negatives, merge ≤12s, refine ±12s at 0.5s, pre-roll 10s, post-roll 15s.
- Padding is applied after logical segmentation and must not merge matches.
- Default export: stream-copy video, drop audio. `--analysis-ready`: H.264 1920×1080 30fps CRF 19–20, no audio, exact boundaries.
- Required CLI: `--output`, `--debug`, `--analysis-ready`, `--scan-interval`, `--pre-roll`, `--post-roll`, `--overwrite`.
- Fail if output artifacts exist unless `--overwrite`. Never delete the source. Scope overwrite to this source's outputs.
- Do not upload `input/`, `.inspection/`, or bulk debug frames.
- Report measured evidence, not hypothetical match counts or accuracy percentages.

## File structure

```text
pyproject.toml
README.md
arena_cutter/
  __init__.py
  __main__.py          # argparse + user-facing errors
  config.py            # profile, ROI, thresholds
  detector.py          # color mask, template score, optional Gladius
  segments.py          # state machine, merge, pad, timestamps, contact-sheet times
  video.py             # ffprobe, scan backends, export, frame extract
  pipeline.py          # orchestration, manifests, review HTML, debug
  templates/linguster_1080p/*.png
tests/
  fixtures/roi/*.png
  test_config.py
  test_detector.py
  test_segments.py
  test_manifest.py
  test_video.py
docs/benchmark-scan-backends.md   # written after the real 20:00–30:00 run
```

## Measured detector constants (lock these)

From 1920×1080 source frames:

- Primary ROI: `x=916, y=36, w=248, h=56`
- Text mask: HSV H 22–36, S ≥ 70, V ≥ 120, B < 150, (R−B) > 35, then 3×1 close
- Score: max over templates of (template-pixel recall), divided by `1 + max(0, mask_on/template_on - 4)/8` when the mask is much denser than the template (rejects the loading-screen logo)
- `positive_threshold = 0.28`, `borderline_threshold = 0.18`
- Fixture evidence: outside/world = 0.000; loading ≈ 0.15; true arena ≥ 0.69 even on sand; line-order and 0/1 remaining match their templates at 1.0
- Gladius ROI (secondary, full frames only): `x=300, y=8, w=240, h=190`

---

### Task 1: Package, config, timestamp helpers

**Files:**
- Create: `pyproject.toml`
- Create: `arena_cutter/__init__.py`
- Create: `arena_cutter/config.py`
- Create: `arena_cutter/segments.py` (timestamp + contact-sheet helpers only in this task's first slice; state machine is Task 2)
- Test: `tests/test_config.py`
- Test: `tests/test_segments.py` (timestamp/contact-sheet cases)

**Interfaces:**
- Consumes: nothing
- Produces:
  - `Roi(x: int, y: int, width: int, height: int)` with `as_ffmpeg_crop() -> str` and `slice(frame) -> np.ndarray`
  - `HsvRange(h_min, h_max, s_min, s_max, v_min, v_max, b_max, rb_min)`
  - `DetectorProfile(name, frame_width, frame_height, primary_roi, gladius_roi, text_hsv, positive_threshold, borderline_threshold, gladius_threshold, templates_dir: Path)`
  - `LINGUSTER_1080P: DetectorProfile`
  - `CutterConfig` dataclass with fields: `scan_interval=2.0`, `entry_window=3`, `entry_positives=2`, `exit_negatives=4`, `merge_gap_seconds=12.0`, `refine_window_seconds=12.0`, `refine_interval=0.5`, `pre_roll=10.0`, `post_roll=15.0`, `profile=LINGUSTER_1080P`, `scan_backend="sequential_ffmpeg"`, `analysis_ready=False`, `debug=False`, `overwrite=False`, `analysis_crf=19`, `analysis_fps=30`, `scan_start: float | None = None`, `scan_end: float | None = None`
  - `UnsupportedProfileError`
  - `require_profile(width: int, height: int, profile: DetectorProfile) -> None`
  - `format_timestamp(seconds: float) -> str` → `H:MM:SS.mmm` with hours unpadded when < 10, minutes/seconds zero-padded (`0:22:16.000`)
  - `contact_sheet_timestamps(start: float, end: float, count: int = 5) -> list[float]` at fractions 0.0, 0.2, 0.5, 0.8, 1.0, clamped, monotonic
  - `sanitize_video_name(name: str) -> str`
  - `clamp(value: float, lo: float, hi: float) -> float`

- [ ] **Step 1: Write failing tests**

```python
from arena_cutter.config import LINGUSTER_1080P, CutterConfig, require_profile, UnsupportedProfileError
from arena_cutter.segments import format_timestamp, contact_sheet_timestamps, clamp, sanitize_video_name

def test_profile_is_1080p_with_measured_roi():
    p = LINGUSTER_1080P
    assert p.frame_width == 1920 and p.frame_height == 1080
    assert (p.primary_roi.x, p.primary_roi.y, p.primary_roi.width, p.primary_roi.height) == (916, 36, 248, 56)
    assert p.primary_roi.as_ffmpeg_crop() == "248:56:916:36"
    assert p.positive_threshold == 0.28
    assert p.borderline_threshold == 0.18

def test_require_profile_rejects_other_dimensions():
    try:
        require_profile(1280, 720, LINGUSTER_1080P)
    except UnsupportedProfileError as exc:
        assert "1920" in str(exc) and "1280" in str(exc)
    else:
        raise AssertionError("expected UnsupportedProfileError")

def test_default_cutter_thresholds():
    c = CutterConfig()
    assert c.scan_interval == 2.0
    assert c.entry_positives == 2 and c.entry_window == 3
    assert c.exit_negatives == 4
    assert c.merge_gap_seconds == 12.0
    assert c.pre_roll == 10.0 and c.post_roll == 15.0

def test_format_timestamp():
    assert format_timestamp(0) == "0:00:00.000"
    assert format_timestamp(1336.0) == "0:22:16.000"
    assert format_timestamp(3600 + 5.25) == "1:00:05.250"

def test_contact_sheet_positions_and_short_clip():
    ts = contact_sheet_timestamps(100, 200, 5)
    assert ts[0] == 100 and ts[-1] == 200
    assert ts == sorted(ts)
    short = contact_sheet_timestamps(5, 6, 5)
    assert short[0] == 5 and short[-1] == 6
    assert len(short) == 5

def test_clamp_and_sanitize():
    assert clamp(-1, 0, 10) == 0
    assert clamp(11, 0, 10) == 10
    assert sanitize_video_name("2v2 SPR +2200.mp4")
    assert "/" not in sanitize_video_name("a/b\\c")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv\Scripts\python.exe -m pytest tests/test_config.py tests/test_segments.py -q`
Expected: FAIL (modules missing)

- [ ] **Step 3: Implement config + helpers**

Implement the dataclasses and functions exactly as in Interfaces. `sanitize_video_name` keeps alphanumerics, `+`, `_`, `-`, `.` and replaces other characters with `_`, stripping `.mp4` for the output folder name.

- [ ] **Step 4: Re-run tests — pass**

- [ ] **Step 5: Commit** `feat: add cutter config profile and time helpers`

---

### Task 2: Segmentation state machine

**Files:**
- Modify: `arena_cutter/segments.py`
- Test: `tests/test_segments.py`

**Interfaces:**
- Consumes: `CutterConfig`, `format_timestamp`, `clamp`
- Produces:
  - `Sample(timestamp: float, positive: bool, borderline: bool, score: float, winning_template: str | None, gladius_present: bool | None)`
  - `GapMerge(gap_start: float, gap_end: float, gap_seconds: float)`
  - `ArenaSegment` with: `raw_start`, `raw_end`, `padded_start`, `padded_end`, `confidence` (`"high"|"medium"|"low"`), `mean_score`, `max_score`, `primary_positive_count`, `gladius_positive_count`, `sample_count`, `merged_gaps: list[GapMerge]`, `truncated_start: bool`, `truncated_end: bool`, `warnings: list[str]`
  - `segment_samples(samples: list[Sample], config: CutterConfig, duration: float) -> list[ArenaSegment]`

Rules to implement (and test):

1. Entry: ≥ `entry_positives` positives in any `entry_window` consecutive samples. Raw start = earliest positive in that window; if the immediately previous sample is borderline, use that earlier timestamp.
2. Isolated single positive (1 of 3) does not start a segment.
3. Exit: `exit_negatives` consecutive negatives that are not borderline. Raw end = last positive or borderline in the span (later, recall-first).
4. Temporary disappearance shorter than exit evidence returns to ARENA.
5. Merge adjacent spans whose raw gap ≤ `merge_gap_seconds` (12s). A 16s world gap (22:16→22:32) must NOT merge.
6. Padding applied after merge: `padded_start = clamp(raw_start - pre_roll, 0, duration)`, `padded_end = clamp(raw_end + post_roll, 0, duration)`. Padding must not change `raw_*` or merge logic.
7. VOD starting/ending in arena: keep the segment; `truncated_start` / `truncated_end` true.
8. Confidence is a label only. Low-confidence persistent segments are retained. `warnings` may include `"low_confidence"`.
9. Very short games (few positives but entry satisfied) are kept.

- [ ] **Step 1: Write failing tests** for: entry 2/3, isolated spike ignored, exit 4 negatives, temporary 2-negative gap stays one segment, 8s gap merges, 16s gap does not, padding 10/15, clamp, truncated flags, low-confidence retained, short game retained.

Helper:

```python
def samples_at(times_and_flags):
    out = []
    for t, flag in times_and_flags:
        positive = flag == "pos"
        borderline = flag == "bord"
        score = 0.9 if positive else (0.22 if borderline else 0.0)
        out.append(Sample(t, positive, borderline, score, "gold_green_22" if positive else None, None))
    return out
```

- [ ] **Step 2: Run — FAIL on missing `segment_samples`**
- [ ] **Step 3: Implement the state machine in `segments.py`**
- [ ] **Step 4: Tests pass**
- [ ] **Step 5: Commit** `feat: add recall-first arena segmentation`

---

### Task 3: Detector + templates + ROI fixtures

**Files:**
- Create: `arena_cutter/detector.py`
- Existing: `arena_cutter/templates/linguster_1080p/*.png` (already extracted)
- Existing: `tests/fixtures/roi/*.png` (already extracted)
- Test: `tests/test_detector.py`

**Interfaces:**
- Consumes: `DetectorProfile`, `LINGUSTER_1080P`, `Roi`, `HsvRange`
- Produces:
  - `FrameScore(timestamp: float | None, primary_score: float, winning_template: str | None, is_positive: bool, is_borderline: bool, gladius_score: float | None, gladius_present: bool | None)`
  - `TemplateBank.load(directory: Path) -> TemplateBank` with `.templates: list[tuple[str, np.ndarray]]` and `.empty -> bool`
  - `text_mask(bgr_roi: np.ndarray, hsv: HsvRange) -> np.ndarray` uint8 0/255
  - `score_mask(mask: np.ndarray, bank: TemplateBank) -> tuple[float, str | None]`
  - `score_roi(bgr_roi, profile, bank) -> FrameScore` (no gladius)
  - `score_frame(bgr_full, profile, bank, timestamp=None, measure_gladius=True) -> FrameScore`
  - `EmptyTemplateBankError`

Scoring: max penalized template recall as measured above. `is_positive` if score ≥ `positive_threshold`. `is_borderline` if not positive and score ≥ `borderline_threshold`. Gladius: only when `measure_gladius` and full frame supplied; otherwise `gladius_score is None` and `gladius_present is None`. Never let Gladius absence force a negative primary.

- [ ] **Step 1: Failing tests** loading each fixture:

```python
FIX = Path(__file__).parent / "fixtures" / "roi"

def score_file(name, bank, profile=LINGUSTER_1080P):
    img = cv2.imread(str(FIX / name))
    return score_roi(img, profile, bank)

def test_positive_fixtures_are_arena(bank):
    for name in ["positive_gold_green.png", "positive_gold_green_dark.png", "positive_green_gold.png", "ending_zero.png", "count_one.png"]:
        s = score_file(name, bank)
        assert s.is_positive, (name, s.primary_score, s.winning_template)

def test_obscured_count_change_still_positive(bank):
    s = score_file("obscured_count_one.png", bank)
    assert s.is_positive

def test_outside_and_loading_are_not_positive(bank):
    for name in ["outside_world.png", "outside_buildings.png", "outside_start.png", "loading.png"]:
        s = score_file(name, bank)
        assert not s.is_positive, (name, s.primary_score)

def test_empty_bank_raises(tmp_path):
    try:
        TemplateBank.load(tmp_path)
    except EmptyTemplateBankError:
        return
    raise AssertionError("expected EmptyTemplateBankError")
```

- [ ] **Step 2: Run — FAIL**
- [ ] **Step 3: Implement detector**
- [ ] **Step 4: Tests pass**
- [ ] **Step 5: Commit** `feat: add linguster 1080p team-status detector`

---

### Task 4: Manifest + review HTML (pure)

**Files:**
- Modify: `arena_cutter/pipeline.py` (pure helpers first)
- Test: `tests/test_manifest.py`

**Interfaces:**
- Consumes: `ArenaSegment`, `format_timestamp`, `CutterConfig`, `VideoMeta` (define a Typed stub in pipeline or video; if `VideoMeta` is not yet implemented, define `VideoMeta` in `video.py` in this task as a dataclass and import it)
- Produces:
  - `VideoMeta(path: Path, duration: float, width: int, height: int, fps: float, video_codec: str, audio_codec: str | None, size_bytes: int)`
  - `match_record(match_number: int, source_name: str, output_name: str, segment: ArenaSegment, profile_name: str, scan_backend: str, export_status: str, export_error: str | None, actual_clip_duration: float | None) -> dict`
  - Required keys: `match_number`, `source_filename`, `output_filename`, `raw_start_s`, `raw_end_s`, `padded_start_s`, `padded_end_s`, `start_timestamp`, `end_timestamp`, `duration_s`, `actual_clip_duration_s`, `confidence`, `mean_score`, `max_score`, `primary_positive_count`, `gladius_positive_count`, `merged_gaps`, `truncated_start`, `truncated_end`, `detector_profile`, `scan_backend`, `export_status`, `export_error`, `warnings`
  - `write_manifests(output_dir: Path, records: list[dict], run_meta: dict) -> None` writes `manifest.csv` and `manifest.json` (JSON includes `matches` plus run-level `source`, `config`, `tool_versions`, `benchmark`, `warnings`)
  - `render_review_html(records: list[dict], sheet_relpaths: list[str]) -> str` with escaped text, relative links `../match_001.mp4`, no server required
  - Failed exports stay in the manifest with `export_status="error"`; successful matches are not removed

- [ ] **Step 1: Failing tests** for required keys, CSV+JSON roundtrip, HTML escaping of `<>&`, relative mp4 links, export failure retained
- [ ] **Step 2: Run — FAIL**
- [ ] **Step 3: Implement helpers**
- [ ] **Step 4: Tests pass**
- [ ] **Step 5: Commit** `feat: add manifests and static review html`

---

### Task 5: Video probe, scan backends, export, contact sheets

**Files:**
- Create/modify: `arena_cutter/video.py`
- Test: `tests/test_video.py`

**Interfaces:**
- Consumes: `Roi`, `CutterConfig`, `DetectorProfile`
- Produces:
  - `probe(path: Path) -> VideoMeta` via ffprobe JSON
  - `iter_seek_frames(path, start, end, interval, roi: Roi | None) -> Iterator[tuple[float, np.ndarray]]` — one FFmpeg timestamp seek per sample
  - `iter_sequential_frames(path, start, end, interval, roi: Roi) -> Iterator[tuple[float, np.ndarray]]` — one FFmpeg decode, crop, `fps=1/interval`. Each yielded timestamp must be a source second (`start + i * interval` plus any PTS parsed from `showinfo`; document which mapping is used). Frames are cropped ROI images when `roi` is set.
  - `extract_frame(path, timestamp: float, roi: Roi | None = None) -> np.ndarray`
  - `export_stream_copy(src, dst, start, end) -> None` video copy, `-an`
  - `export_analysis_ready(src, dst, start, end, crf=19, fps=30) -> None` libx264 1920×1080 30fps no audio
  - `write_contact_sheet(labeled_bgr_frames: list[tuple[str, np.ndarray]], dest: Path) -> None` five labeled frames, labels are SOURCE timestamps
  - `ffmpeg_version() -> str`, `ffprobe_version() -> str`
  - `FfmpegError` on missing binary / non-zero exit
  - `verify_clip_decodable(path: Path) -> float` probes duration; raises if no video stream / cannot decode first frame

Tests without the 3GB VOD:

- Fake ffprobe JSON via a thin wrapper or by testing `parse_ffprobe_json(payload)`
- Timestamp mapping: `scheduled_timestamps(start, end, interval)` is exclusive-end, includes start, last value ≤ end
- Contact sheet writer on synthetic numpy frames produces a readable image file
- Stream-copy command construction includes `-an` and `copy`
- Analysis-ready command construction includes `libx264`, `1920:1080` or `1920x1080`, `30`, `crf`, `-an`

- [ ] **Step 1: Failing tests**
- [ ] **Step 2: Run — FAIL**
- [ ] **Step 3: Implement video.py**
- [ ] **Step 4: Tests pass**
- [ ] **Step 5: Commit** `feat: add ffmpeg scan and export backends`

---

### Task 6: Pipeline CLI, debug, overwrite, refinement

**Files:**
- Create: `arena_cutter/__main__.py`
- Modify: `arena_cutter/pipeline.py`
- Test: `tests/test_cli.py`, `tests/test_pipeline.py`

**Interfaces:**
- Consumes: all previous
- Produces:
  - `parse_args(argv: list[str] | None) -> argparse.Namespace`
  - `run_pipeline(source: Path, output_root: Path, config: CutterConfig) -> Path` returns the run directory `output_root/<sanitized>/`
  - Coarse scan using `config.scan_backend` (`sequential_ffmpeg` or `seek`)
  - Refine each coarse boundary in ±`refine_window_seconds` at `refine_interval` with `extract_frame` / a short sequential window; ambiguous → earlier start, later end
  - Export each padded segment; probe actual duration
  - Write manifests, `review/match_XXX.jpg`, `review/index.html`
  - `--debug`: write `debug/samples.csv` (timestamp, score, template, state), ROI masks for boundary samples, state transitions, merge decisions, FFmpeg commands; do not dump every full frame
  - Overwrite: if run dir has `match_*.mp4` or `manifest.json` and not `overwrite`, raise `OutputExistsError` before exporting
  - One export failure records error and continues
  - CLI maps `UnsupportedProfileError`, missing ffmpeg, unreadable file to non-zero exit and a clear message

Required usage:

```text
python -m arena_cutter "input/my_vod.mp4"
python -m arena_cutter "input/my_vod.mp4" --output output --debug
python -m arena_cutter "input/my_vod.mp4" --analysis-ready
```

- [ ] **Step 1: Failing tests** for argparse flags, overwrite guard, refinement earlier-start/later-end on synthetic scores, debug sample CSV columns
- [ ] **Step 2: Run — FAIL**
- [ ] **Step 3: Implement pipeline + CLI**
- [ ] **Step 4: Tests pass**
- [ ] **Step 5: Commit** `feat: add arena cutter pipeline and CLI`

---

### Task 7: Benchmark 20:00–30:00, excerpts, full VOD, README

**Files:**
- Create: `arena_cutter/benchmark.py` (callable as `python -m arena_cutter.benchmark`)
- Create: `docs/benchmark-scan-backends.md`
- Create: `README.md`

Benchmark on the sample file, window 1200–1800s, interval 2s:

1. Seek backend wall-clock, sample count, first/last timestamp, detector positives
2. Sequential backend same
3. Reliability: expected ~300 samples, timestamps monotonic and within 0.5×interval of schedule, classifications equivalent (or document diffs)
4. Winner: faster reliable method; if within 20%, prefer sequential
5. Record actual numbers. Do not claim a benchmark that was not run.

Then excerpt validation (internal `scan_start`/`scan_end`, `--debug`, inspect sheets and clip starts):

- 1240–1280 world vs residual HUD
- 1280–1340 match including result
- 1330–1365 result → world → next prep (must not merge 22:16–22:32)

Then one full-VOD run with the chosen backend. Inspect every review sheet. Report misses/merges/false positives honestly. Do not invent 30–50 matches or 95% accuracy.

- [ ] **Step 1: Run benchmark, write `docs/benchmark-scan-backends.md` with elapsed time, counts, timestamp check, classification diffs, chosen backend**
- [ ] **Step 2: Point `CutterConfig.scan_backend` default at the winner; commit config if it changed**
- [ ] **Step 3: Excerpt runs + inspect**
- [ ] **Step 4: Full VOD run once**
- [ ] **Step 5: README with exact venv, Python version, run commands, output layout, limitations**
- [ ] **Step 6: Commit** `docs: record scan benchmark, README, and run instructions`

---

## Spec coverage

| Spec section | Task |
| --- | --- |
| Canonical 1080p ROI / unsupported dimensions | 1, 3 |
| HSV mask + template bank, both line orders, counts | 3 |
| Gladius secondary only | 3, 6 |
| Coarse scan benchmark 20:00–30:00 | 7 |
| State machine, merge 12s, padding 10/15, recall bias | 2 |
| Boundary refinement ±12s @ 0.5s | 6 |
| Fast copy + analysis-ready export | 5, 6 |
| Manifests, review HTML, contact sheets | 4, 5, 6 |
| CLI flags, overwrite, debug | 6 |
| Automated fixture + segmentation tests | 2, 3, 4 |
| Full-VOD human review | 7 |

## Type consistency

`Sample`, `ArenaSegment`, `FrameScore`, `VideoMeta`, `CutterConfig`, `DetectorProfile`, `Roi` names are used identically in every task. `scan_backend` values are `"sequential_ffmpeg"` and `"seek"`. Output clip names are `match_{n:03d}.mp4`.
