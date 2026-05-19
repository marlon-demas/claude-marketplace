# marlon-demas — Claude Code skills marketplace

Personal marketplace for cross-platform Claude Code automation skills.

## Plugins

### android-emulator-skill (v0.1.0)

The Android-side parallel to `conorluddy/ios-simulator-skill`. Used by the `makes-design` plugin's verify loop on hosts that cannot run Xcode (Windows, Linux).

10 Phase-1 scripts cover AVD lifecycle (list / boot / shutdown), app management (install APK / launch activity), capture (screenshot / accessibility dump / logcat), and interaction (tap / swipe).

See [android-emulator-skill/skills/android-emulator-skill/SKILL.md](./android-emulator-skill/skills/android-emulator-skill/SKILL.md) for usage.

## Requirements

- Python 3.9+
- Android SDK platform-tools (`adb`)
- Android SDK emulator (`emulator`)
- At least one AVD

## License

MIT
