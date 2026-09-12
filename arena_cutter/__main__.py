from __future__ import annotations

import argparse
import sys
from pathlib import Path

from arena_cutter.config import CutterConfig, UnsupportedProfileError
from arena_cutter.detector import EmptyTemplateBankError
from arena_cutter.pipeline import OutputExistsError, run_pipeline
from arena_cutter.video import FfmpegError


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="arena_cutter",
        description="Detect and export WoW arena sessions from a single VOD.",
    )
    parser.add_argument("source", help="Path to one source MP4")
    parser.add_argument("--output", default="output", help="Output root directory")
    parser.add_argument("--debug", action="store_true", help="Keep detector debug artifacts")
    parser.add_argument("--analysis-ready", action="store_true", help="Re-encode clips for analysis")
    parser.add_argument("--scan-interval", type=float, default=2.0)
    parser.add_argument("--pre-roll", type=float, default=10.0)
    parser.add_argument("--post-roll", type=float, default=15.0)
    parser.add_argument("--overwrite", action="store_true", help="Replace artifacts for this source")
    return parser.parse_args(argv)


def config_from_args(args: argparse.Namespace) -> CutterConfig:
    return CutterConfig(
        scan_interval=args.scan_interval,
        pre_roll=args.pre_roll,
        post_roll=args.post_roll,
        analysis_ready=args.analysis_ready,
        debug=args.debug,
        overwrite=args.overwrite,
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    source = Path(args.source)
    if not source.is_file():
        print(f"source not found: {source}", file=sys.stderr)
        return 2
    try:
        run_dir = run_pipeline(source, Path(args.output), config_from_args(args))
    except (UnsupportedProfileError, EmptyTemplateBankError, FfmpegError, OutputExistsError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"wrote {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
