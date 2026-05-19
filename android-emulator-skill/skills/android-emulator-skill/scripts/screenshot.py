#!/usr/bin/env python3
"""Capture a PNG screenshot via `adb exec-out screencap -p`."""
from __future__ import annotations

import argparse
import os
import subprocess

from _common import add_common_flags, emit, fail, output_mode, require_tool, resolve_serial


def capture(serial: str, output_path: str) -> int:
    """Capture screen to PNG. Returns byte size of the file."""
    adb = require_tool("adb")
    cmd = [adb, "-s", serial, "exec-out", "screencap", "-p"]
    with open(output_path, "wb") as f:
        proc = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, timeout=30)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace").strip() or "screencap failed")
    return os.path.getsize(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture an Android emulator screenshot")
    parser.add_argument("--output", default="screenshot.png", help="Destination PNG path")
    add_common_flags(parser)
    args = parser.parse_args()
    mode = output_mode(args)

    try:
        serial = resolve_serial(args.serial)
        size = capture(serial, args.output)
    except Exception as e:
        fail(str(e), mode=mode)

    if size == 0:
        fail("Screenshot file is empty", mode=mode)

    emit(
        {"output": args.output, "size_bytes": size, "serial": serial, "success": True},
        summary=f"Saved {args.output} ({size} bytes) from {serial}",
        mode=mode,
    )


if __name__ == "__main__":
    main()
