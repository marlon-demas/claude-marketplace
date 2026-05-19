---
name: android-emulator-skill
version: 0.1.0
description: 10 production scripts for Android emulator testing and automation. Boot AVDs, install APKs, launch activities, screenshot, accessibility-dump (uiautomator), tap / swipe, capture logcat, and shutdown. Cross-platform (macOS, Linux, Windows). The Android-side parallel to ios-simulator-skill, used by the makes-design verify loop when the host cannot run Xcode.
---

# Android Emulator Skill

Boot Android emulators, install builds, drive UI, and capture state — accessibility-tree first, screenshots second. The Android-side parallel to `ios-simulator-skill`.

**Why this skill exists:** `ios-simulator-skill` is macOS-only. Windows and Linux contributors building Expo / React Native / Flutter apps need the same verify primitives (boot, install, screenshot, a11y audit, gesture drive, log capture) but on Android tooling.

## Quick Start

```bash
# 1. List available AVDs
python scripts/list_avds.py

# 2. Boot an AVD (e.g. Pixel_6_API_34) — waits for sys.boot_completed
python scripts/boot_emulator.py --avd Pixel_6_API_34

# 3. Install an APK
python scripts/install_apk.py --apk ./app-debug.apk

# 4. Launch the app
python scripts/launch_activity.py --package com.example.app --activity .MainActivity

# 5. Screenshot to PNG
python scripts/screenshot.py --output ./shot.png

# 6. Dump accessibility hierarchy as JSON
python scripts/a11y_dump.py --json
```

All scripts support `--help` (options), `--verbose` (human-readable detail), and `--json` (machine-parseable).

## Navigation Strategy

**Always prefer the accessibility tree (`a11y_dump.py`) over screenshots for navigation.** uiautomator returns a structured XML hierarchy with `content-desc`, `text`, `class`, `bounds`, and `clickable` flags — far cheaper and more reliable than image analysis.

Use this priority:
1. `a11y_dump.py --json` → structured element list (10-50 tokens default, full tree on `--verbose`)
2. `tap.py` / `swipe.py` with coordinates derived from a11y dump bounds
3. `screenshot.py` → only for visual verification, anti-slop check, or bug reports

## 10 Phase-1 Scripts

### Lifecycle (3)

1. **list_avds.py** — Enumerate AVDs installed via `avdmanager`
   - Output: name list, default format 1 line each
   - Options: `--json`, `--verbose`

2. **boot_emulator.py** — Boot AVD by name; wait for `getprop sys.boot_completed=1`
   - Options: `--avd <name>`, `--timeout <seconds>`, `--no-window`, `--port <emulator-port>`, `--json`, `--verbose`

3. **shutdown.py** — Cleanly stop a running emulator
   - Options: `--serial <serial>` (auto-detects single device), `--json`, `--verbose`

### App management (2)

4. **install_apk.py** — Install or reinstall an APK
   - Options: `--apk <path>`, `--serial <serial>` (optional), `--json`, `--verbose`

5. **launch_activity.py** — Start the main activity of an installed package
   - Options: `--package <id>`, `--activity <name>` (default `.MainActivity`), `--serial`, `--json`, `--verbose`

### Capture (3)

6. **screenshot.py** — Capture a PNG via `adb exec-out screencap -p`
   - Options: `--output <path>` (default `screenshot.png`), `--serial`, `--json`, `--verbose`

7. **a11y_dump.py** — Dump UI hierarchy via `uiautomator dump`, parse XML, emit JSON or terse summary
   - Options: `--serial`, `--filter clickable|focusable|all`, `--json`, `--verbose`

8. **logcat.py** — Capture recent device logs
   - Options: `--serial`, `--lines <N>` (default 100), `--filter <tag>`, `--severity E|W|I|D`, `--json`, `--verbose`

### Interaction (2)

9. **tap.py** — Tap a screen coordinate
   - Options: `--x <int>`, `--y <int>`, `--serial`, `--json`, `--verbose`

10. **swipe.py** — Swipe between two coordinates
    - Options: `--from x,y`, `--to x,y`, `--duration <ms>` (default 300), `--serial`, `--json`, `--verbose`

## Common Patterns

**Auto-serial detection**: Scripts auto-detect the serial when exactly one emulator is running. Pass `--serial` explicitly if multiple are connected.

**Output Formats**: Default is concise (3-5 lines, ~5-10 tokens). `--verbose` gives detail (~50+ lines). `--json` is machine-parseable.

**Help**: All scripts support `--help`.

**Exit codes**: 0 on success; non-zero on failure with a clear stderr message.

## Requirements

- Python 3.9+
- Android SDK platform-tools on PATH (provides `adb`)
- Android SDK emulator on PATH (provides `emulator`)
- At least one AVD created via `avdmanager` or Android Studio (Pixel_6_API_34 recommended)
- No third-party Python packages — stdlib only

### One-time setup (Windows / Linux / macOS)

```bash
# Verify tools
adb version
emulator -list-avds

# Create an AVD if none exist (requires Android Studio or sdkmanager)
sdkmanager "system-images;android-34;google_apis;x86_64"
avdmanager create avd --name Pixel_6_API_34 --package "system-images;android-34;google_apis;x86_64" --device "pixel_6"
```

## Phase 2 (not yet implemented)

- `type_text.py` — Keyboard input
- `long_press.py`, `pinch.py` — Advanced gestures
- `navigator.py` — Semantic find-and-tap by `content-desc` / `text`
- `visual_diff.py` — Screenshot comparison
- `health_check.sh` — Environment verification (parallel to `sim_health_check.sh`)

## Integration with makes-design

This skill is wrapped by the `makes-design` plugin's `verify` skill when the project's stack profile is `expo-rn` or `flutter` AND `verifyTarget: android` (or `both`) is set in `.makes-design/contract.yml`. The verify loop calls these scripts to capture screenshots, dump the a11y tree, and run anti-slop checks against the chosen direction's Signature.

## Design Principles

**Semantic over pixel-based**: Find via uiautomator content-desc / text; tap with derived coordinates.

**Token-efficient**: Default output stays under 10 tokens; opt into `--verbose` or `--json` when needed.

**No-shell-True**: All `subprocess` calls pass argv lists, never raw shell strings.

**Stdlib-only**: No PIP install step required after `adb` and `emulator` are on PATH.

**Cross-platform**: Tested on macOS, Ubuntu, and Windows 11 (PowerShell + WSL2).
