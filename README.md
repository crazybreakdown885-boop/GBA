# GBA Enhanced (Android)

An Android-focused Game Boy Advance emulator build. The emulation engine is **SkyEmu**, an established open-source emulator supporting GBA, GB, GBC and (beta) Nintendo DS. The Android build includes its native emulation core, touchscreen controls, gamepad support, save states, fast-forward/rewind and display shaders.

## Build and download

Every push to `main` builds an Android release APK using GitHub Actions and updates the `v0.1.1` GitHub Release with the APK attached.

The workflow checks out the reviewed SkyEmu source revision `b64903f0fde8104d0796546b96859e9f682311b7`, changes the displayed app name to GBA Enhanced, and builds its Android project with the Android NDK.

## Current functionality

- Actual GBA emulation via SkyEmu (not a mock screen).
- Android touchscreen input and supported physical controllers.
- ROM opening through Android's file picker / file association, including `.zip` archives containing a `.gba`, `.gb`, `.gbc` or `.nds` ROM (the first supported ROM in the archive is extracted safely).\n- Compact Android interface scaling and Portuguese UI translations when the device language is Portuguese.
- Save states, fast-forward, rewind and built-in display shaders from the upstream engine.
- Game Boy and Game Boy Color support; Nintendo DS support is beta upstream.

## Requested enhancements not yet implemented

- Automatic game analysis that reconstructs 3D geometry from 2D GBA frames. This cannot be made universal by a simple filter; it needs game-specific assets, depth maps or reconstruction profiles.
- Dynamic 3D scene shadows. The upstream core does not expose a general 3D scene for 2D GBA games.
- Per-game widescreen hacks. These require game-specific ROM patches or camera/game logic modifications; stretching the original 3:2 image is not equivalent and may distort gameplay.

These features are not represented as working toggles until implemented and tested. Existing display shaders can improve pixel presentation but do not convert a game's artwork into true 3D.

## Licensing

SkyEmu is MIT-licensed. Its source is fetched by the build workflow and its license/copyright notices are retained in the upstream checkout. This project does not bundle commercial My Boy code or copyrighted game ROMs. Supply your own legally obtained ROM files.
