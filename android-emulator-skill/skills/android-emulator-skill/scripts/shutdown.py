#!/usr/bin/env python3
"""Cleanly shutdown a running emulator."""
from __future__ import annotations

import argparse

from _common import add_common_flags, emit, fail, output_mode, resolve_serial, run_adb


def main() -> None:
    parser = argparse.ArgumentParser(description="Shutdown a running Android emulator")
    add_common_flags(parser)
    args = parser.parse_args()
    mode = output_mode(args)

    try:
        serial = resolve_serial(args.serial)
    except Exception as e:
        fail(str(e), mode=mode)

    result = run_adb(["emu", "kill"], serial=serial)
    if not result.ok:
        fail(result.stderr.strip() or "emu kill failed", mode=mode)

    emit(
        {"serial": serial, "success": True},
        summary=f"Shutdown sent to {serial}",
        mode=mode,
    )


if __name__ == "__main__":
    main()
