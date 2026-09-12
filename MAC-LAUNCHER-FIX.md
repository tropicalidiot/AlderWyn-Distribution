# Mac launcher packaging repair — macfix1

The original launcher could be rejected by macOS as damaged. It lacked a complete bundle signature and placed managed .NET files alongside executable code without the bundle structure required for strict signing.

The replacement ZIPs end in **macfix1.zip**, with bundle build number 2. The launcher and game version remain 0.1.0; this is a packaging repair.

## Install the replacement

1. Download the **Intel** replacement if your Mac has an Intel processor, or **Apple silicon** for M-series Macs, using the links in README.md.
2. Extract it using Finder's built-in Archive Utility. Keep the app bundle intact.
3. Replace your earlier **AlderWyn Launcher.app** with this copy, then open it. Existing installed-game data is stored separately.
4. The launcher requires **macOS 14 or newer**. It includes .NET; installing a separate .NET runtime is unnecessary.

These packages have ad-hoc development signatures, not a paid Developer ID identity or Apple notarization. If you receive an **unidentified developer** / **Apple cannot check** message, Apple's supported per-app option is **System Settings → Privacy & Security → Open Anyway**, if offered. [Apple instructions](https://support.apple.com/en-us/102445).

If the repaired copy still says **damaged**, report the exact macOS version and warning. The packaging checks do not certify browser-quarantine Gatekeeper acceptance. Do not disable Gatekeeper or remove quarantine globally.

## Changes and verification

- Managed assemblies and configuration live in `Contents/Resources`; native libraries live in `Contents/Frameworks`. Relative links preserve .NET's self-contained runtime lookup.
- Native libraries and helper executables are signed before the app bundle is sealed using Apple's `codesign`. JIT entitlement is included for the main app.
- Apple's strict recursive signature verification passes, including after packaging and fresh extraction with `ditto`.
- Native apphost startup and the launcher renderer execute on Intel and Apple silicon macOS runners.
- LaunchServices opens the app and produces a completed launcher rendering.
- All of these checks ran in [this successful manual Mac verification](https://github.com/tropicalidiot/AlderWyn-Distribution/actions/runs/34717957946).

The tests use the actual Mac binary with the launcher's render mode. They do not certify all interactive controls, native Unity gameplay, or Gatekeeper acceptance of a browser-downloaded app. No Apple Developer credentials are embedded in these packages. The workflow runs only when manually dispatched.
