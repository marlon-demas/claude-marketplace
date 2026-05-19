"""Shared helpers for android-emulator-skill scripts.

Stdlib-only. No third-party packages.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import dataclass


class ToolMissing(RuntimeError):
    """Raised when a required external tool (adb, emulator) is not on PATH."""


@dataclass
class AdbResult:
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def require_tool(name: str) -> str:
    """Return absolute path to a required tool, or raise ToolMissing."""
    path = shutil.which(name)
    if not path:
        raise ToolMissing(
            f"Required tool '{name}' not found on PATH. "
            "Install Android SDK platform-tools and emulator, then add them to PATH."
        )
    return path


def run_adb(args: list[str], serial: str | None = None, timeout: float | None = 30.0) -> AdbResult:
    """Run an adb command. No shell=True, ever."""
    adb = require_tool("adb")
    cmd = [adb]
    if serial:
        cmd += ["-s", serial]
    cmd += args
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        return AdbResult(returncode=124, stdout=e.stdout or "", stderr=f"adb timed out after {timeout}s")
    return AdbResult(returncode=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)


def list_devices() -> list[str]:
    """Return serial numbers of connected emulators / devices in 'device' state."""
    result = run_adb(["devices"])
    if not result.ok:
        return []
    serials: list[str] = []
    for line in result.stdout.splitlines()[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            serials.append(parts[0])
    return serials


def resolve_serial(explicit: str | None) -> str:
    """Return a usable device serial, auto-detecting if exactly one is connected."""
    if explicit:
        return explicit
    serials = list_devices()
    if not serials:
        raise RuntimeError("No emulator detected. Boot one with `boot_emulator.py --avd <name>`.")
    if len(serials) > 1:
        raise RuntimeError(
            f"Multiple devices detected ({', '.join(serials)}). "
            "Pass --serial <serial> to disambiguate."
        )
    return serials[0]


def emit(payload: dict, *, summary: str, mode: str) -> None:
    """Emit output in one of three modes: default (terse), verbose, or json.

    - default: a single line summary
    - verbose: summary then pretty key=value lines
    - json: machine-parseable JSON to stdout
    """
    if mode == "json":
        print(json.dumps(payload, indent=None, separators=(",", ":")))
        return
    print(summary)
    if mode == "verbose":
        for k, v in payload.items():
            print(f"  {k}: {v}")


def fail(message: str, *, mode: str = "default", code: int = 1) -> None:
    """Print a structured error and exit non-zero."""
    if mode == "json":
        print(json.dumps({"success": False, "error": message}))
    else:
        print(f"Error: {message}", file=sys.stderr)
    sys.exit(code)


def output_mode(args) -> str:
    if getattr(args, "json", False):
        return "json"
    if getattr(args, "verbose", False):
        return "verbose"
    return "default"


def add_common_flags(parser) -> None:
    """Attach --verbose / --json / --serial to a parser. --serial is optional everywhere."""
    parser.add_argument("--verbose", action="store_true", help="Detailed human-readable output")
    parser.add_argument("--json", action="store_true", help="Machine-parseable JSON output")
    parser.add_argument("--serial", default=None, help="Target device serial (auto-detected if single device)")
