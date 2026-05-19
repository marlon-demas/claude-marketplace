#!/usr/bin/env python3
"""Install or reinstall an APK on the emulator."""
from __future__ import annotations

import argparse
import os

from _common import add_common_flags, emit, fail, output_mode, resolve_serial, run_adb


def main() -> None:
    parser = argparse.ArgumentParser(description="Install an APK on the Android emulator")
    parser.add_argument("--apk", required=True, help="Path to .apk file")
    add_common_flags(parser)
    args = parser.parse_args()
    mode = output_mode(args)

    if not os.path.isfile(args.apk):
        fail(f"APK not found: {args.apk}", mode=mode)

    try:
        serial = resolve_serial(args.serial)
    except Exception as e:
        fail(str(e), mode=mode)

    result = run_adb(["install", "-r", args.apk], serial=serial, timeout=180)
    if not result.ok:
        fail(result.stderr.strip() or result.stdout.strip() or "install failed", mode=mode)

    emit(
        {"apk": args.apk, "serial": serial, "success": True},
        summary=f"Installed {os.path.basename(args.apk)} on {serial}",
        mode=mode,
    )


if __name__ == "__main__":
    main()
