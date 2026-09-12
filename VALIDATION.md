# Release 0.1.0 validation

## Launcher repair follow-up

The original launchers failed the user's Mac opening check. The **macfix1** replacements correct the bundle layout and apply complete development signatures. Native Intel and Apple silicon macOS 15.7.9 checks now pass: strict Apple signature verification, direct apphost rendering, LaunchServices rendering, and signature verification after ZIP extraction. [Repair details and remaining Gatekeeper limits](MAC-LAUNCHER-FIX.md). The historical Windows-only results below describe the original delivery; native game testing and notarization remain outstanding.

## Completed on Windows, 12 September 2026

- Unity 6000.4.12f1 macOS Mono build succeeded: **0 errors**, 365 warnings. Warnings include package compute-shader variants and deprecated editor APIs; the build is not warning-free.
- The build explicitly includes `OutdoorCrafting.unity` as its playable scene.
- All **7 native binaries in the game ZIP** contain both x86_64 and arm64 architectures.
- All three ZIPs passed archive CRC checks. Native executable entries retain Unix execute permissions.
- The Apple silicon and Intel launchers contain the correct `tropicalidiot/AlderWyn-Distribution` configuration.
- GitHub confirmed SHA-256 and byte sizes for all three uploaded assets.
- **30 shared-service tests passed**, covering install, update, restart recovery, corrupt downloads, cancellation, offline state, archive safety and settings persistence.
- **11 native Avalonia interface checks passed** using an isolated unconfigured test fixture for navigation, settings, errors and guide display.
- A separate configured launcher screenshot fetched the real public manifest and displayed latest version **0.1.0**.
- **8 live distribution checks passed** using the production downloader, hash checker, archive extractor, installer and manifest reader against the public GitHub URLs, with no GitHub credentials. A fresh installation completed, the next check reported Current, and a simulated network outage preserved installed-game availability.

The live installation check used production Mac bundle validation with a Windows test adapter for platform availability and process detection. It did **not** execute the Mac game or simulate a successful native launch.

## Still requires a Mac

- Open the launcher and actual game on Apple silicon / Intel; test gameplay, rendering, audio and process detection.
- Verify Gatekeeper behavior, executable permissions after Mac extraction, launch preferences and folder selection.
- Perform the real two-release install → play → update → play exercise from SETUP.md. Version-changing service tests have passed, but only one public game release currently exists.
- Developer ID signing, notarization and stapling for production distribution. These packages are development previews and are not Apple-notarized.

The initial distribution pipeline is connected and verified through installation. Native Mac acceptance testing and a signed production release remain separate steps.
