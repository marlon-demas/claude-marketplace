#!/usr/bin/env python3
"""Tap a screen coordinate via `adb shell input tap`."""
from __future__ import annotations

import argparse

from _common import add_common_flags, emit, fail, output_mode, resolve_serial, run_adb


def main() -> None:
    parser = argparse.ArgumentParser(description="Tap a coordinate on the Android emulator")
    parser.add_argument("--x", type=int, required=True)
    parser.add_argument("--y", type=int, required=True)
    add_common_flags(parser)
    args = parser.parse_args()
    mode = output_mode(args)

    try:
        serial = resolve_serial(args.serial)
    except Exception as e:
        fail(str(e), mode=mode)

    result = run_adb(["shell", "input", "tap", str(args.x), str(args.y)], serial=serial)
    if not result.ok:
        fail(result.stderr.strip() or "input tap failed", mode=mode)

    emit(
        {"x": args.x, "y": args.y, "serial": serial, "success": True},
        summary=f"Tapped ({args.x}, {args.y}) on {serial}",
        mode=mode,
    )


if __name__ == "__main__":
    main()
