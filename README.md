# AlderWyn — Downloads and updates

AlderWyn is a cozy crafting game in development. This repository serves the macOS launcher, packaged game releases, update manifest and patch notes.

## Download

- [Launcher for Apple silicon Macs](https://github.com/tropicalidiot/AlderWyn-Distribution/releases/download/v0.1.0/AlderWyn-Launcher-v0.1.0-osx-arm64.zip)
- [Launcher for Intel Macs](https://github.com/tropicalidiot/AlderWyn-Distribution/releases/download/v0.1.0/AlderWyn-Launcher-v0.1.0-osx-x64.zip)
- [Game only — universal macOS build](https://github.com/tropicalidiot/AlderWyn-Distribution/releases/download/v0.1.0/AlderWyn-mac-v0.1.0.zip)
- [Release notes](patchnotes/0.1.0.md)

The launcher requires macOS 14 or later. Extract the correct launcher ZIP, open **AlderWyn Launcher.app**, then choose **Install AlderWyn**. After installation, choose **Play AlderWyn**. Future game versions are detected through this repository. Players do not need GitHub credentials, .NET or Unity installed.

These are **unsigned development previews**, built on Windows with macOS build tools. Native Mac launch/gameplay testing and Apple signing/notarization remain outstanding. macOS may block an unsigned application; follow [Apple's per-app guidance](https://support.apple.com/en-gb/102445) only for a build you trust. Do not disable Gatekeeper globally. This is not yet a signed production release.

## Playing

Use **WASD** to move, the **mouse** to turn the third-person camera, and **Shift** to run. Approach a crafting station and press **E**. Choose a recipe, start crafting, then return to collect the completed items. The preview contains the outdoor crafting clearing, sawmill, workbench and smelter. Multiplayer and hosted servers are not included.

## Updating

The launcher reads [manifest.json](https://raw.githubusercontent.com/tropicalidiot/AlderWyn-Distribution/main/manifest.json), downloads the matching release asset, checks its SHA-256, and safely replaces the installed game. Previously installed games support offline play.

For developers, [SETUP.md](SETUP.md) explains the manual build → package → release → manifest process and a two-version update test. Version 0.1.0 is the initial release; increment to 0.1.1 or later for the next real game update. The launcher itself does not automatically update itself.

Only public distribution files belong here. Unity source, signing credentials and private development files remain outside this repository. Release ZIPs are attached to GitHub Releases, never committed into the repository history.
