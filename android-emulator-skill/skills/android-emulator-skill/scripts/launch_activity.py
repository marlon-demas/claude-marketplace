#!/usr/bin/env python3
"""Launch an Android activity via `am start`."""
from __future__ import annotations

import argparse

from _common import add_common_flags, emit, fail, output_mode, resolve_serial, run_adb


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch an Android app activity")
    parser.add_argument("--package", required=True, help="Package id, e.g. com.example.app")
    parser.add_argument("--activity", default=".MainActivity", help="Activity name (relative or fully-qualified)")
    add_common_flags(parser)
    args = parser.parse_args()
    mode = output_mode(args)

    try:
        serial = resolve_serial(args.serial)
    except Exception as e:
        fail(str(e), mode=mode)

    component = f"{args.package}/{args.activity}"
    result = run_adb(["shell", "am", "start", "-n", component], serial=serial)
    if not result.ok or "Error" in result.stdout:
        fail(result.stderr.strip() or result.stdout.strip() or "am start failed", mode=mode)

    emit(
        {"component": component, "serial": serial, "success": True},
        summary=f"Launched {component} on {serial}",
        mode=mode,
    )


if __name__ == "__main__":
    main()
