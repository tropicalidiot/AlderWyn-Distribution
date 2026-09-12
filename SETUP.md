# Set up AlderWyn Launcher and GitHub updates

**Mac launcher repair:** use downloads ending in `macfix1.zip` from GitHub. These have complete development signatures and passed native Intel and Apple silicon startup and archive checks. The original Windows-packaged launcher archives are superseded. For details, see [Mac repair instructions](https://github.com/tropicalidiot/AlderWyn-Distribution/blob/main/MAC-LAUNCHER-FIX.md). Future `bundle.py` packaging must run on macOS; it signs the bundle, preserves relative links with `ditto`, and verifies a fresh extraction. Apple notarization remains outstanding.

Your launcher is now configured for [tropicalidiot/AlderWyn-Distribution](https://github.com/tropicalidiot/AlderWyn-Distribution). Download the matching launcher from that repository's Releases page. The manual instructions below also explain how to repeat setup for another repository and publish future updates. Your Unity source stays private; only packaged builds, the public manifest and patch notes are distributed.

The initial game release is **0.1.0**. For your next game update use **0.1.1** (or a later semantic version), replacing the tutorial's 0.0.1 / 0.0.2 examples accordingly. The checked-in launcher configuration already contains `tropicalidiot`; no placeholder needs editing for your repository. Native Mac launch testing and Apple signing/notarization still require a Mac.

## 1. What you need

- A GitHub account and a Mac on which you can build and run AlderWyn.
- macOS 14 or later for this .NET 10 launcher. Microsoft lists supported versions in its [.NET 10 support table](https://github.com/dotnet/core/blob/main/release-notes/10.0/supported-os.md).
- Unity with its macOS build support installed.
- The .NET 10 **SDK** to build the launcher from source. Players do not need the SDK or runtime when using a self-contained launcher bundle.
- Python 3.11 or later if using the included packaging/manifest helpers. Manual commands are also shown below.

Choose the launcher archive matching your Mac: `osx-arm64` for Apple silicon, `osx-x64` for Intel. Extract the ZIP on your Mac; it contains **AlderWyn Launcher.app**. The delivered bundles were compiled on Windows and are unsigned development builds. They still require the native validation checklist at the end of this guide. They are not a notarized public release.

## 2. Create the public distribution repository

1. Sign into GitHub in your browser.
2. Click **+** near the top right, then **New repository**.
3. Select your account as owner and enter **AlderWyn-Distribution** as the name.
4. Select **Public**. Public access lets the launcher read the manifest and download releases without credentials. Never embed a GitHub token in this launcher.
5. Enable **Add a README file**, then click **Create repository**.
6. The default branch should be `main`. If it differs, use its actual name in the launcher configuration and URLs below.

The recommended repository structure is:

```text
AlderWyn-Distribution/
    README.md
    manifest.json
    patchnotes/
        0.0.1.md
        0.0.2.md
```

Copy the starter files from this launcher's `distribution` folder using **Add file → Upload files**, or commit them with Git. The example manifest deliberately has an invalid placeholder checksum and size until you replace them with a real game ZIP. Do not publish it as a working release before those values are correct.

Game ZIPs go in **GitHub Releases**, not normal repository commits. Do not upload the Unity `Assets`, `Library`, `ProjectSettings`, private source, credentials, signing certificates or secrets. Your separate Unity source repository does not need to be public.

## 3. Configure the launcher in one place

Open `src/AlderWyn.Launcher/distribution.json` in the launcher source:

```json
{
  "owner": "YOUR_GITHUB_USERNAME",
  "repository": "AlderWyn-Distribution",
  "branch": "main"
}
```

Replace the username with the account that owns the distribution repository. This one file determines the trusted repository and raw manifest address. There are no other owner/repository constants to edit.

The resulting manifest address is:

```text
https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/AlderWyn-Distribution/main/manifest.json
```

To verify it manually, open `manifest.json` in GitHub and click **Raw**. The browser should show JSON, not a GitHub webpage or a sign-in form. This raw URL is what the launcher fetches at startup and when you click **Check for updates**.

Rebuild the launcher after changing this file. For local unsigned development you can also edit the copy inside **AlderWyn Launcher.app → Show Package Contents → Contents/MacOS/distribution.json**. Editing a signed bundle invalidates its signature; production changes require rebuilding, signing and notarizing again.

## 4. Build the first game version in Unity

1. Open your AlderWyn Unity project on the Mac.
2. Set **Project Settings → Player → Version** to `0.0.1`. Make sure the product name is **AlderWyn**.
3. Open **File → Build Profiles** (older Unity versions call this **Build Settings**).
4. Add/select **macOS**. If macOS support is absent, install it through Unity Hub for the editor version you are using.
5. Switch to that profile/platform if necessary.
6. Include the playable scene in the build's scene list.
7. Choose **Intel + Apple silicon / Universal** if the same game ZIP should work on both Mac architectures. A single-architecture game ZIP only supports that architecture; the current `macos` manifest entry represents one game asset.
8. Click **Build**, choose an output folder, and name the product **AlderWyn**.
9. Confirm the result is **AlderWyn.app**, then open it directly and test movement, crafting and quitting before packaging.

The launcher build and game build are different apps. The launcher installs `AlderWyn.app`; it must not download and install its own `AlderWyn Launcher.app` as the game. Unity's [macOS build documentation](https://docs.unity3d.com/6000.0/Documentation/Manual/macos-building.html) explains the architecture options.

## 5. Package the game without damaging the app bundle

On the Mac, open Terminal and change into the folder containing `AlderWyn.app`. For example:

```sh
cd "$HOME/Desktop/AlderWynBuild"
ditto -c -k --sequesterRsrc --keepParent "AlderWyn.app" "AlderWyn-mac-v0.0.1.zip"
```

The ZIP must have `AlderWyn.app` at its top level, with its complete `Contents` folder. Do not ZIP only the executable or an extra enclosing build folder. `ditto` preserves the bundle's file permissions and links. Keep the original build as your working copy.

Inspect before uploading:

```sh
unzip -l "AlderWyn-mac-v0.0.1.zip" | head -20
```

Look for `AlderWyn.app/Contents/Info.plist` and `AlderWyn.app/Contents/MacOS/…`.

## 6. Get the SHA-256 and byte size

Run this exact checksum command:

```sh
shasum -a 256 AlderWyn-mac-v0.0.1.zip
```

It prints a 64-character hexadecimal checksum, followed by the filename. Copy only the 64-character checksum into the manifest's `sha256` field. Repackaging or changing even one byte changes the checksum; calculate it from the exact ZIP you upload.

Get the size in **bytes**, not Finder's rounded megabyte display:

```sh
stat -f%z AlderWyn-mac-v0.0.1.zip
```

Copy that integer into `size` without quotes.

## 7. Publish the GitHub Release

1. Open **AlderWyn-Distribution** on GitHub.
2. Open **Releases** on the repository page, then **Draft a new release** or **Create a new release**.
3. Choose/create the tag **v0.0.1**, targeting `main`.
4. Enter a release title such as **AlderWyn v0.0.1** and describe the changes.
5. Drag **AlderWyn-mac-v0.0.1.zip** into the release assets upload area. Wait for upload to finish.
6. Click **Publish release**. Keep the first test release public and accessible without login.

Game version `0.0.1`, release tag `v0.0.1`, and ZIP filename `AlderWyn-mac-v0.0.1.zip` must correspond. GitHub's [release guide](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) describes the current UI.

On the published release, right-click the uploaded ZIP and copy its link. It should be:

```text
https://github.com/YOUR_GITHUB_USERNAME/AlderWyn-Distribution/releases/download/v0.0.1/AlderWyn-mac-v0.0.1.zip
```

Use the uploaded ZIP link, not GitHub's automatically generated **Source code (zip)** archive. Test the download link in a private browser window to confirm that it does not require authentication.

## 8. Publish the manifest and patch notes

The complete manifest shape is:

```json
{
  "launcherVersion": "0.1.0",
  "gameVersion": "0.0.1",
  "platforms": {
    "macos": {
      "url": "https://github.com/USERNAME/AlderWyn-Distribution/releases/download/v0.0.1/AlderWyn-mac-v0.0.1.zip",
      "sha256": "COPY_THE_REAL_64_CHARACTER_CHECKSUM_HERE",
      "size": 123456789
    }
  },
  "patchNotes": {
    "version": "0.0.1",
    "url": "https://raw.githubusercontent.com/USERNAME/AlderWyn-Distribution/main/patchnotes/0.0.1.md"
  }
}
```

This is a template: the checksum and size cannot be correct until a real ZIP exists. To generate a working manifest with the actual checksum and size automatically, run the included helper from the launcher source folder:

```sh
python3 scripts/create-manifest.py YOUR_GITHUB_USERNAME AlderWyn-Distribution 0.0.1 "/full/path/AlderWyn-mac-v0.0.1.zip" > manifest.json
```

| Field | Meaning |
|---|---|
| `launcherVersion` | Version of the launcher source, currently `0.1.0`; this field does not trigger launcher self-updates |
| `gameVersion` | Semantic game version without a leading `v`, such as `0.0.1` |
| `platforms` | Map of platform-specific downloadable builds |
| `macos` | Current supported game platform; use a Universal game build for both Mac architectures |
| `url` | Public GitHub Release asset URL for the exact game version |
| `sha256` | Exact 64-character SHA-256 of the uploaded ZIP |
| `size` | Exact ZIP size in bytes, stored as an integer |
| `patchNotes.version` | Game version described by the notes |
| `patchNotes.url` | Raw GitHub URL to the notes file in the same distribution repository |

Replace `USERNAME` in both URLs. Replace the repository name if you chose a different one. Update version, tag, filename, checksum, size and patch-note URL together for each release.

Create `patchnotes/0.0.1.md` with the actual tested changes. Commit/push the notes and completed `manifest.json` to `main` **after** the matching ZIP is downloadable. You can use GitHub's **Add file → Create new file** and **Commit changes** without a local Git installation.

## 9. Build the launcher on Mac

From the launcher source folder, after editing `distribution.json`:

```sh
dotnet run --project tests/AlderWyn.Launcher.Tests -- artifacts/mac-tests.json
bash scripts/build-macos.sh osx-arm64
```

Use `osx-x64` instead for Intel. The script publishes a self-contained .NET app, adds its `Info.plist`, and creates a fresh timestamped artifact folder. Its output includes **AlderWyn Launcher.app** and a ZIP with the executable's Unix permissions. Extract the ZIP on the target Mac rather than copying an unpacked bundle through a filesystem that discards executable permissions.

For a direct development launch from source:

```sh
dotnet run --project src/AlderWyn.Launcher
```

Avalonia documents the [Mac app bundle structure and signing process](https://docs.avaloniaui.net/docs/deployment/macos). Do not treat the delivered cross-built bundles as Mac-tested until you run the checks below.

## 10. First release and update test

1. **Publish v0.0.1** and its manifest as above.
2. Run the configured launcher with no installed game. Expected: **Install AlderWyn**, latest `v0.0.1`.
3. Click Install. Expected: actual progress, SHA-256 verification, safe extraction, then **Play AlderWyn**.
4. Click Play. Confirm the Unity game opens. The default launcher behavior is Minimize. Quit the game.
5. Make a visible game change, set Unity's version to `0.0.2`, and build `AlderWyn.app` again.
6. Package **AlderWyn-mac-v0.0.2.zip**, calculate its new checksum/size, and publish GitHub release **v0.0.2**.
7. Add `patchnotes/0.0.2.md` and update all relevant manifest fields to `0.0.2`. Commit/push the manifest after the ZIP is available.
8. Reopen the launcher or click **Updates → Check for updates**. Expected: installed `v0.0.1`, latest `v0.0.2`, and **Update AlderWyn**.
9. Click Update. Expected: download and verification complete, old game protected during replacement, local manifest becomes `0.0.2`.
10. Click Play and confirm the visible change in the new build. Restart the launcher; it should still report `v0.0.2` as current.

Also test offline launch by disconnecting the network after installation. Play must remain available. Test cancellation during a new download and a deliberate wrong checksum in a temporary test manifest: the previous working game must still open. Restore the correct manifest immediately after that test. Keep test releases separate from any release real players use.

This two-release exercise requires your GitHub identity, real Mac game builds and a Mac. It has not been claimed as completed merely because the local service tests pass.

## 11. Settings and local files

On Mac the default location is:

```text
~/Library/Application Support/AlderWynData/
    Game/
        AlderWyn.app
    launcher_data/
        local_manifest.json
        settings.json
        logs/launcher.log
        updates/incoming/
        updates/extracted/
```

Settings lets you choose a user-writable game folder, open it, enable automatic game updates, enable launch after an update, and select Stay open / Minimize / Close after launch. Changing the folder selects a different installation; it does not move or delete the previous one. The local manifest includes its installation path to avoid confusing two installations.

The updater temporarily creates `.alderwyn-stage-…` and `.alderwyn-backup-…` inside the selected Game folder so the final rename stays on one filesystem. A journal in `launcher_data` restores an interrupted replacement. Leave those files alone while an update is active. The launcher finishes recovery on its next start.

## 12. Troubleshooting

| Problem | What to check |
|---|---|
| Manifest 404 | Confirm username, repository, branch and `manifest.json` spelling. Open the Raw link without signing in. |
| ZIP 404 | Confirm the release is published, tag is `v…`, filename/capitalization matches, and the asset upload finished. Do not use Source code ZIP. |
| Wrong username/repository | Fix `distribution.json`, rebuild, and ensure both manifest URLs use the same identity. |
| Hash mismatch | Recompute SHA-256 from the uploaded ZIP. If you repackaged it, upload the new asset and publish its new hash. Never bypass verification. |
| File size mismatch | Use `stat -f%z`, not rounded MB. Confirm the manifest refers to the exact uploaded file. |
| App missing or invalid ZIP layout | Use `ditto --keepParent` on `AlderWyn.app` itself. Its `Contents` must remain intact and at the expected level. |
| Extraction fails | Check free disk space and permissions; read `launcher.log`. The previous game remains protected. |
| Cannot write files | Select a folder in your home directory. Do not use a protected system folder or request admin rights. |
| Executable has no permission | Repackage the original working app on Mac using `ditto`. Do not flatten it or distribute it through tooling that loses Unix modes. |
| macOS refuses to launch | Inspect the OS security message and the game's own startup logs. Check the architecture and signing status. See Gatekeeper below. |
| Game already running | Quit AlderWyn fully, then retry. The launcher does not kill a running game to update it. |
| Manifest version seems unchanged | Confirm the commit is on the configured branch and visible through the Raw URL. GitHub caching can take a short time; retry. |
| No update detected | Increase `gameVersion`, not just `launcherVersion`. `0.0.10` is newer than `0.0.2`; a newer local game is not automatically downgraded. |
| Corrupted settings | Defaults are used and a warning is displayed. The damaged file is kept until you explicitly save new settings. |
| Corrupted local manifest | The game can still launch if its bundle is valid, but the installed version shows unknown. A verified install/update writes a fresh manifest. |
| No internet/GitHub unavailable | Installed games can still Play. Without an installed game, wait for connectivity and retry. |
| GitHub rate/connectivity errors | Retry later, inspect the public URLs and network/proxy settings. There is no token to reset or secret to add. |

Technical details are written to `launcher_data/logs/launcher.log` (with one rotated previous log). User messages stay concise. Release notes failing to load do not block the installed game.

## 13. Gatekeeper, signing and notarization

Unsigned development apps may trigger a macOS warning. Read the exact warning and verify that the app is your trusted local build. Apple explains the per-app process in [Open apps safely on your Mac](https://support.apple.com/en-gb/102445). Do not disable Gatekeeper globally, remove security protections, or automatically strip quarantine attributes in the launcher.

The long-term release process is to sign with an **Apple Developer ID Application** certificate, enable hardened runtime with the appropriate .NET JIT entitlement, notarize with Apple, and staple the ticket before packaging. Sign both your Unity game and launcher through their supported workflows. `scripts/Launcher.entitlements` contains the basic JIT entitlement for review; your final signing configuration must be validated on the target Mac. Signing and notarization require your Apple account/certificate and macOS tools and are not completed by a Windows cross-build.

Before public distribution, verify on Apple silicon and Intel as applicable: app launch, first install, actual Unity process detection, blocked update while running, update/restart, in-bundle symlinks, executable modes, offline Play, chooser/save/open-folder behavior, cancellation, and Stay open / Minimize / Close. Record the Mac and OS version used. The shared service suite can run on Mac as an additional check; it uses a process test double and does not replace a real launch test.

## 14. Windows later and optional automation

Future releases can include both `AlderWyn-mac-v0.1.0.zip` and `AlderWyn-win-v0.1.0.zip`. Add a `windows` entry alongside `macos`, then implement `WindowsGamePlatform` and select it in `PlatformService`. The shared manifest/downloader/checksum/update logic stays reusable. Windows game installation is deliberately disabled in this version.

The first workflow remains manual: build → ZIP → hash → create release → upload → update manifest. Once the two-release test above succeeds, GitHub Actions or Unity build automation can perform those same steps. No CI/CD, accounts, login, servers, matchmaking, regions or multiplayer features are required or active here.
