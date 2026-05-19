#!/usr/bin/env python3
"""Swipe between two coordinates via `adb shell input swipe`."""
from __future__ import annotations

import argparse

from _common import add_common_flags, emit, fail, output_mode, resolve_serial, run_adb


def parse_xy(spec: str) -> tuple[int, int]:
    parts = spec.split(",")
    if len(parts) != 2:
        raise ValueError(f"Expected 'x,y' got '{spec}'")
    return int(parts[0]), int(parts[1])


def main() -> None:
    parser = argparse.ArgumentParser(description="Swipe between two coordinates on the Android emulator")
    parser.add_argument("--from", dest="src", required=True, help="Starting coordinate as x,y")
    parser.add_argument("--to", dest="dst", required=True, help="Ending coordinate as x,y")
    parser.add_argument("--duration", type=int, default=300, help="Swipe duration in milliseconds (default 300)")
    add_common_flags(parser)
    args = parser.parse_args()
    mode = output_mode(args)

    try:
        x1, y1 = parse_xy(args.src)
        x2, y2 = parse_xy(args.dst)
        serial = resolve_serial(args.serial)
    except Exception as e:
        fail(str(e), mode=mode)

    result = run_adb(
        ["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(args.duration)],
        serial=serial,
    )
    if not result.ok:
        fail(result.stderr.strip() or "input swipe failed", mode=mode)

    emit(
        {"from": [x1, y1], "to": [x2, y2], "duration_ms": args.duration, "serial": serial, "success": True},
        summary=f"Swiped ({x1},{y1}) -> ({x2},{y2}) in {args.duration}ms on {serial}",
        mode=mode,
    )


if __name__ == "__main__":
    main()
