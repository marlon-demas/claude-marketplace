#!/usr/bin/env python3
"""List installed Android Virtual Devices (AVDs) via the `emulator` CLI."""
from __future__ import annotations

import argparse
import subprocess

from _common import emit, fail, output_mode, require_tool


def list_avds() -> list[str]:
    emulator = require_tool("emulator")
    proc = subprocess.run([emulator, "-list-avds"], capture_output=True, text=True, timeout=10)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "emulator -list-avds failed")
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="List installed Android AVDs")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    mode = output_mode(args)

    try:
        avds = list_avds()
    except Exception as e:
        fail(str(e), mode=mode)

    if not avds:
        emit({"avds": [], "count": 0}, summary="No AVDs found. Create one with `avdmanager create avd`.", mode=mode)
        return

    summary = f"{len(avds)} AVD(s): " + ", ".join(avds)
    emit({"avds": avds, "count": len(avds)}, summary=summary, mode=mode)


if __name__ == "__main__":
    main()
