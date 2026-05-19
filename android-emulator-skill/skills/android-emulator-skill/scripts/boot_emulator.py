#!/usr/bin/env python3
"""Boot an AVD and wait for sys.boot_completed=1."""
from __future__ import annotations

import argparse
import subprocess
import time

from _common import emit, fail, list_devices, output_mode, require_tool, run_adb


def start_emulator(avd: str, *, port: int | None, no_window: bool) -> subprocess.Popen:
    emulator = require_tool("emulator")
    cmd = [emulator, "-avd", avd]
    if port:
        cmd += ["-port", str(port)]
    if no_window:
        cmd.append("-no-window")
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def wait_for_boot(timeout: float) -> str:
    """Wait for a new device to appear AND for sys.boot_completed=1. Return its serial."""
    deadline = time.time() + timeout
    before = set(list_devices())
    serial: str | None = None

    while time.time() < deadline:
        current = set(list_devices())
        new = current - before
        if new:
            serial = sorted(new)[0]
            break
        time.sleep(1.5)

    if not serial:
        raise TimeoutError(f"No new device appeared within {timeout}s")

    while time.time() < deadline:
        result = run_adb(["shell", "getprop", "sys.boot_completed"], serial=serial, timeout=5)
        if result.ok and result.stdout.strip() == "1":
            return serial
        time.sleep(2)

    raise TimeoutError(f"Device {serial} did not finish booting within {timeout}s")


def main() -> None:
    parser = argparse.ArgumentParser(description="Boot an Android emulator AVD")
    parser.add_argument("--avd", required=True, help="AVD name (see list_avds.py)")
    parser.add_argument("--timeout", type=float, default=120.0, help="Total boot timeout in seconds")
    parser.add_argument("--port", type=int, default=None, help="Optional emulator console port")
    parser.add_argument("--no-window", action="store_true", help="Headless boot (no UI window)")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    mode = output_mode(args)

    start = time.time()
    try:
        start_emulator(args.avd, port=args.port, no_window=args.no_window)
        serial = wait_for_boot(args.timeout)
    except Exception as e:
        fail(str(e), mode=mode)

    elapsed = round(time.time() - start, 1)
    summary = f"Booted {args.avd} on {serial} [{elapsed}s]"
    emit(
        {"avd": args.avd, "serial": serial, "elapsed_seconds": elapsed, "success": True},
        summary=summary,
        mode=mode,
    )


if __name__ == "__main__":
    main()
