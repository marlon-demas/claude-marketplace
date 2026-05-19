#!/usr/bin/env python3
"""Capture recent device logs via `adb logcat`."""
from __future__ import annotations

import argparse

from _common import add_common_flags, emit, fail, output_mode, resolve_serial, run_adb


SEVERITIES = {"E": "Error", "W": "Warning", "I": "Info", "D": "Debug", "V": "Verbose"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture recent Android logcat output")
    parser.add_argument("--lines", type=int, default=100, help="Number of trailing lines (default 100)")
    parser.add_argument("--filter", default=None, help="Tag filter, e.g. ActivityManager")
    parser.add_argument(
        "--severity",
        choices=list(SEVERITIES.keys()),
        default=None,
        help="Minimum severity (E/W/I/D/V)",
    )
    add_common_flags(parser)
    args = parser.parse_args()
    mode = output_mode(args)

    try:
        serial = resolve_serial(args.serial)
    except Exception as e:
        fail(str(e), mode=mode)

    cmd = ["logcat", "-d", "-t", str(args.lines)]
    if args.filter:
        tag_spec = f"{args.filter}:{args.severity or 'V'}"
        cmd += [tag_spec, "*:S"]
    elif args.severity:
        cmd += [f"*:{args.severity}"]

    result = run_adb(cmd, serial=serial, timeout=20)
    if not result.ok:
        fail(result.stderr.strip() or "logcat failed", mode=mode)

    lines = [ln for ln in result.stdout.splitlines() if ln.strip()]

    if mode == "json":
        emit({"serial": serial, "count": len(lines), "lines": lines, "success": True}, summary="", mode="json")
        return

    summary = f"{len(lines)} log line(s) from {serial}"
    print(summary)
    if mode == "verbose":
        for ln in lines:
            print(ln)


if __name__ == "__main__":
    main()
