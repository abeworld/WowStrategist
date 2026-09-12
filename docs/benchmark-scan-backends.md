# Scan backend benchmark

Source: `2v2 SPR +2200 MMR _ January 5th Stream VOD _ WOW R1 Gladiator Rogue Arena PVP - Warmane WOTLK.mp4`
Window: 0:20:00.000 – 0:30:00.000 (1200–1800s)
Interval: 2.0s

## Timing

| Backend | Elapsed (s) | Samples | Positives | First ts | Last ts |
| --- | ---: | ---: | ---: | ---: | ---: |
| seek | 74.80 | 301 | 240 | 1200.0 | 1800.0 |
| sequential_ffmpeg | 12.04 | 301 | 239 | 1200.0 | 1800.0 |

## Timestamp reliability

| Backend | OK | Monotonic | Expected count | Max abs error (s) | Tolerance (s) |
| --- | --- | --- | ---: | ---: | ---: |
| seek | True | True | 301 | 0.0 | 1.0 |
| sequential_ffmpeg | True | True | 301 | 0.0 | 1.0 |

Classification disagreements (aligned timestamps): 1

## Known-event checkpoints

- arena ~20:00: seek=1200.0s positive score=0.998; sequential=1200.0s positive score=0.998
- world ~20:50: seek=1250.0s negative score=0.000; sequential=1250.0s negative score=0.000
- result ~22:14: seek=1334.0s positive score=0.933; sequential=1334.0s positive score=0.933
- world ~22:16: seek=1336.0s negative score=0.000; sequential=1336.0s negative score=0.000
- prep ~22:32: seek=1352.0s positive score=0.952; sequential=1352.0s positive score=0.952

## Choice

Selected backend: **sequential_ffmpeg**

Rule: faster reliable method; if elapsed times differ by no more than 20%, prefer sequential FFmpeg.
