# WowStrategist

Arena VOD cutter plus a static 2v2 encyclopedia.

Live encyclopedia: https://abeworld.github.io/WowStrategist/

# Arena cutter

Local Python tool that takes one World of Warcraft arena VOD, detects each arena session from the top-center Gold/Green team-status block, and exports one MP4 per match plus manifests and a static review page.

V1 is tuned to Linguster's 1920×1080 Warmane WotLK layout. Other dimensions fail with an explicit unsupported-profile error.

## Setup (Windows)

FFmpeg and ffprobe must be on `PATH`. Python 3.13 is the tested interpreter (3.14 may work if OpenCV wheels are available):

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest
```

## Run

```powershell
.\.venv\Scripts\python.exe -m arena_cutter "input\your_vod.mp4"
.\.venv\Scripts\python.exe -m arena_cutter "input\your_vod.mp4" --output output --debug
.\.venv\Scripts\python.exe -m arena_cutter "input\your_vod.mp4" --analysis-ready
```

Options: `--output`, `--debug`, `--analysis-ready`, `--scan-interval`, `--pre-roll`, `--post-roll`, `--overwrite`.

Existing artifacts for the same source are not replaced unless `--overwrite` is passed. The source file is never deleted.

## Outputs

```text
output/<sanitized-video-name>/
  match_001.mp4
  manifest.csv
  manifest.json
  review/index.html
  review/match_001.jpg
```

Open `review/index.html` locally (no server). Each contact sheet is five source-timestamped frames.

Default export stream-copies video and drops audio (keyframe alignment can make the physical cut slightly earlier than requested). `--analysis-ready` re-encodes H.264 1920×1080 30 fps, CRF 19, no audio, using the refined timestamps.

## Detector

The primary signal is the two-line block:

```text
Gold Team: N Players Remaining
Green Team: N Players Remaining
```

present during preparation, combat, deaths, and the result screen, and absent in Dalaran/queue and loading screens. Line order can swap. Gladius is secondary corroboration only and is not required for preparation rooms.

Recall is preferred over neat boundaries: uncertain starts expand earlier, uncertain ends expand later, gaps up to 8 seconds merge, and low-confidence persistent segments are labeled rather than dropped. A 12-second merge window glued consecutive games across short loading screens on the sample VOD, so the default is 8 seconds. The documented 16-second Dalaran gap at 22:16–22:32 still stays split.

## Benchmark

Compare coarse scan backends on a 10-minute window:

```powershell
.\.venv\Scripts\python.exe -m arena_cutter.benchmark "input\your_vod.mp4"
```

Results are written to `docs/benchmark-scan-backends.md`. The pipeline default follows that choice.

## Limitations

- 1920×1080 Linguster UI only.
- Nameplates and raid markers can cover the team-status text; persistence is meant to ride through brief occlusion.
- Stream-copy cuts follow source keyframes (~5 s on the sample).
- Fast requeues (~10 s including loading) are usually split into two clips. If the team-status block disappears for longer than the exit window before the result screen, the scoreboard can become its own short clip.
- A long sitting in arena, or a requeue so fast the team-status block never stays absent for 8 s, can still produce one oversized clip covering two games.
- Match count and accuracy are whatever the review page shows for a given VOD — not a claimed percentage.
