# WoW Arena Auto-Cutter — MVP Design

Date: 2026-09-04

## Objective

Build a small, deterministic local Python tool that turns one long Warmane WotLK arena VOD from the target player/UI into one MP4 per arena match plus CSV/JSON manifests and fast review artifacts.

The MVP detects and cuts matches only. Strategy analysis, OCR, class/spec detection, combat interpretation, downloading, and a sophisticated UI are out of scope.

Recall has priority over precision. A slightly oversized clip or occasional false-positive clip is acceptable; a missed match or clipped opener is not.

## Evidence From the Sample VOD

The inspected source is 1:45:02, 1920×1080, 60 fps, H.264 at approximately 4.1 Mbps with AAC audio. Its keyframes are consistently spaced about 5.07 seconds apart.

The strongest arena-session signal is the fixed two-line status block near the top center:

- `Gold Team: N Players Remaining`
- `Green Team: N Players Remaining`

The block is present during preparation, active combat, player deaths, and the result screen. It is absent in normal Dalaran/queue footage and loading screens. The line order can change, and the count can be 0, 1, or 2.

Gladius is useful corroborating evidence during active combat but is not reliable for arena entry because it may be absent during preparation. The `Shadow Sight` objective can remain visible briefly after returning to Dalaran and must not define session boundaries.

A representative observed sequence was:

- approximately 22:10: final opponent dying;
- approximately 22:14: result screen;
- approximately 22:16: returned to Dalaran and the team-status block disappeared;
- approximately 22:30: next queue prompt;
- approximately 22:32: next preparation room and the team-status block returned.

## Detection Approach

### Canonical frame and ROI

The V1 detector profile supports the sample's 1920×1080 layout. Other dimensions produce a clear unsupported-profile error instead of silently applying the wrong ROI. Proportional scaling for other 16:9 inputs can be added only after the 1080p profile is validated.

Only a top-center region around the team-status block is scored. Exact coordinates will be fixed from the sample and stored in one configuration profile for this player's 1080p UI.

### Primary signal

The detector isolates the gold/green UI text from the moving background using HSV/color masking and light morphological cleanup. It then compares the binary mask to a small template bank extracted from the sample.

The bank covers:

- both possible Gold/Green line orders;
- the normal 2/2 preparation and combat state;
- representative 1-player and 0-player ending states.

The maximum normalized template score is the primary per-frame arena score. This is deterministic and does not use OCR.

### Secondary evidence

A second fixed ROI looks for the characteristic two-row Gladius panel. It only raises confidence or rescues an otherwise borderline primary frame. Its absence never blocks arena detection.

Loading-screen and general-HUD observations may be recorded for debugging, but V1 does not require a dedicated map or loading-screen classifier.

## Coarse Scan Benchmark

Two coarse-scan implementations will be built behind the same frame-source interface:

1. **Sequential FFmpeg pipe:** decode once, crop and scale before transfer where possible, sample the ROI at approximately 0.5 fps, and stream timestamped ROI frames to Python.
2. **Repeated timestamp seeking:** request one frame every approximately 2 seconds with OpenCV/FFmpeg seeking, which may decode forward from the preceding H.264 keyframe.

Both will be benchmarked against the same 20:00–30:00 source window, which contains outside footage, several transitions, preparation, combat, and endings. The benchmark records wall-clock time, number of samples, timestamp accuracy, and detector-equivalent output.

The faster reliable method wins. Reliability requires the expected number of samples, monotonically increasing timestamps within half a scan interval of their target times, and equivalent detector classifications on the benchmark window. If both are reliable and their wall-clock times differ by no more than 20%, prefer the sequential FFmpeg pipe because it has simpler timing behavior and avoids thousands of independent seeks. The benchmark result and selected backend are recorded in the debug/run metadata. Only the selected backend is used for the full-VOD integration run.

The initial scan cadence is configurable and defaults to 2 seconds.

## State Machine and Recall Bias

The logical states are:

`OUTSIDE → CANDIDATE → ARENA → EXIT_CANDIDATE → OUTSIDE`

Initial thresholds are centralized in configuration rather than spread through the code:

- entry: at least 2 positive samples among 3 consecutive coarse samples;
- exit: 4 consecutive negative samples;
- logical gap merge: merge adjacent arena spans separated by no more than 12 seconds;
- start padding: 10 seconds before the refined first positive;
- end padding: 15 seconds after the refined last positive.

Padding does not merge logical matches; it is applied after segmentation and may create harmless overlap between exported clips.

Recall-first behavior is explicit:

- ambiguous entry expands earlier;
- ambiguous exit expands later;
- an uncertain short negative gap is merged rather than split;
- confidence is informational and never a reason to silently discard an otherwise plausible segment;
- a single weak isolated frame may be ignored, but a persistent or strongly corroborated candidate is exported even at low confidence;
- segments touching the beginning or end of the VOD are retained and marked accordingly.

This preserves VODs that begin or end during an arena and very short games. The normal preparation period supplies substantial evidence even when combat itself is brief.

## Boundary Refinement

Each coarse entry and exit is rescanned within an approximately ±12-second window at 0.5-second intervals using the same detector.

The raw start is the earliest sustained positive near entry. The raw end is the last positive near exit, including count changes and score-screen frames. Configurable start/end padding is then applied and clamped to the source duration.

If refinement remains ambiguous, the cutter selects the earlier start and later end. It does not attempt to detect gates opening or the exact killing blow.

## Export Modes

### Default fast mode

FFmpeg stream-copies the video and drops audio. Keyframe alignment may make the physical clip slightly more generous than the requested boundary, which is consistent with the recall-first policy.

### `--analysis-ready`

FFmpeg re-encodes to H.264 at 1080p and 30 fps with no audio. The initial quality target is CRF 19–20 with a conventional preset, preserving small icons, health bars, buffs, and debuffs. This mode uses precise refined boundaries.

Neither mode upscales a lower-resolution source.

## Outputs

For an input video, output is written beneath `output/<sanitized-video-name>/`:

```text
match_001.mp4
match_002.mp4
...
manifest.csv
manifest.json
review/
  match_001.jpg
  match_002.jpg
  ...
  index.html
```

Each manifest entry includes at least:

- match number and output filename;
- source filename;
- raw and padded source start/end seconds;
- formatted start/end timestamps and duration;
- confidence label and numeric score summary;
- primary-positive sample count and gap information;
- Gladius corroboration summary;
- boundary/VOD-edge flags;
- detector profile and scan backend.

JSON also contains source metadata, configuration values, benchmark metadata, tool versions, and run-level warnings.

## Review and Debug Artifacts

Each match receives a labeled five-frame contact sheet showing approximately:

- beginning;
- early match;
- middle;
- near end;
- final frame.

Sampling adapts for short clips so frames remain ordered and distinct where possible. The static HTML review page presents each sheet, source timestamps, duration, confidence, warnings, and a link to the MP4. It requires no server and no frontend framework.

With `--debug`, the run also keeps:

- timestamped transition frames;
- primary ROI images and binary masks;
- matched template and score for each retained boundary sample;
- per-sample score data;
- state-transition and merge decisions;
- benchmark details and FFmpeg commands;
- the detector profile/templates used.

## CLI

Primary usage:

```text
python -m arena_cutter input/my_vod.mp4
```

Initial options:

```text
--output <directory>
--debug
--analysis-ready
--scan-interval <seconds>
--pre-roll <seconds>
--post-roll <seconds>
--overwrite
```

Single-file processing is the MVP. Folder processing is deferred.

## Code Organization

```text
arena_cutter/
  __init__.py
  __main__.py
  config.py
  detector.py
  segments.py
  video.py
  pipeline.py
  templates/
    linguster_1080p/
tests/
```

- `config.py`: profiles and centralized thresholds.
- `detector.py`: ROI preprocessing, template scores, and optional Gladius evidence.
- `segments.py`: state machine, persistence, merging, padding, and confidence summaries.
- `video.py`: ffprobe metadata, scan backends, boundary frames, FFmpeg export, and thumbnails.
- `pipeline.py`: orchestration, manifests, debug artifacts, and review page.
- `__main__.py`: argument parsing and user-facing errors.

Dependencies are limited to Python, OpenCV, NumPy, and installed FFmpeg/ffprobe. HTML, CSV, JSON, and process execution use the standard library. OpenCV is not currently installed in the workspace environment and will need to be added before execution.

## Error Handling

The CLI fails clearly for missing FFmpeg/ffprobe, unreadable video, absent video stream, unsupported dimensions/layout, empty detector template bank, and export failures. One failed clip export is reported in the manifest/run summary and does not erase successfully generated clips.

Existing output is not silently overwritten. By default the CLI fails before export if target artifacts already exist; `--overwrite` explicitly permits replacement of artifacts for that same source run. Temporary files stay inside the run output and are cleaned only after successful finalization; debug mode retains them when useful.

## Testing and Verification

Automated tests cover deterministic behavior:

- template-score fixtures for positive, ending, outside, and loading frames;
- entry/exit persistence;
- temporary negative gaps;
- adjacent-session merging and non-merging;
- VOD beginning or ending in arena;
- recall-first low-confidence retention;
- boundary refinement and padding calculations;
- timestamp formatting;
- CSV/JSON manifest generation;
- contact-sheet frame-position calculations.

Development uses short representative excerpts rather than repeatedly processing the full VOD:

- world → arena preparation;
- one complete arena and return to world;
- two consecutive games with a short gap;
- ending/count-change and result-screen sequence.

After targeted tests and excerpt validation pass, the chosen coarse backend runs once over the full 1:45 sample. Final verification checks detected-count plausibility, every review sheet, edge cases/warnings, clip readability, and spot-checks of start/end boundaries. No success claim is made solely from automated tests; the generated review page remains the human acceptance artifact.

## MVP Acceptance Criteria

- Almost every genuine match in the representative VOD is exported.
- False clips are uncommon but tolerated.
- A genuine match normally maps to exactly one logical clip.
- Preparation and openers are retained.
- Deaths, outcomes, and score screens are retained.
- Review artifacts make the entire run quick to inspect.
- Detector decisions are explainable from saved scores and images.
- No cloud or AI service is used.
