---
title: "StillMotion Local Server Download | macOS, Linux, Windows"
description: "Browse your PC media from iPhone and iPad over LAN. Zero configuration, QR code pairing. Available for macOS, Linux, and Windows. Free."
download:
  appSlug: "stillmotion"
  releases:
    - version: "1.1"
      githubRelease: "stillmotion-server-v1.1"
      files:
        - platform: "macOS (Apple Silicon)"
          filename: "StillMotion-Server-1.1.dmg"
          url: "https://github.com/iidatakumi/homepage/releases/download/stillmotion-server-v1.1/StillMotion-Server-1.1.dmg"
          size: "5.9MB"
          note: "Recommended. DMG installer"
        - platform: "macOS (Apple Silicon)"
          filename: "stillmotion-server-darwin-arm64"
          url: "https://github.com/iidatakumi/homepage/releases/download/stillmotion-server-v1.1/stillmotion-server-darwin-arm64"
          size: "6.7MB"
          note: "CLI binary"
        - platform: "macOS (Intel)"
          filename: "stillmotion-server-darwin-amd64"
          url: "https://github.com/iidatakumi/homepage/releases/download/stillmotion-server-v1.1/stillmotion-server-darwin-amd64"
          size: "7.1MB"
          note: "CLI binary"
        - platform: "Linux (x86_64)"
          filename: "stillmotion-server-linux-amd64"
          url: "https://github.com/iidatakumi/homepage/releases/download/stillmotion-server-v1.1/stillmotion-server-linux-amd64"
          size: "6.9MB"
          note: "CLI binary"
        - platform: "Linux (ARM64)"
          filename: "stillmotion-server-linux-arm64"
          url: "https://github.com/iidatakumi/homepage/releases/download/stillmotion-server-v1.1/stillmotion-server-linux-arm64"
          size: "6.6MB"
          note: "Raspberry Pi, etc."
        - platform: "Windows (x86_64)"
          filename: "stillmotion-server-windows-amd64.exe"
          url: "https://github.com/iidatakumi/homepage/releases/download/stillmotion-server-v1.1/stillmotion-server-windows-amd64.exe"
          size: "7.1MB"
          note: "Double-click to run"
        - platform: "Windows (ARM64)"
          filename: "stillmotion-server-windows-arm64.exe"
          url: "https://github.com/iidatakumi/homepage/releases/download/stillmotion-server-v1.1/stillmotion-server-windows-arm64.exe"
          size: "6.6MB"
          note: "Double-click to run"
---

## StillMotion Local Server

Your PC media, on your device.

Browse photos and videos on your PC directly from the StillMotion app, over LAN.
No internet required. Pair with a QR code.

### Features

- **Zero configuration** -- Download, launch, done. No setup needed.
- **QR code pairing** -- Scan a QR code from the app to connect instantly.
- **Thumbnail generation** -- Server-side thumbnails reduce data transfer.
- **Web admin panel** -- Browser-based UI to manage media roots.
- **Security** -- LAN-only communication. Token-based authentication.

### Setup Guide

1. Download and launch
2. The admin panel opens automatically in your browser
3. Set your media folders
4. Enable sharing
5. Scan the QR code from the StillMotion app to connect

### About ffmpeg

ffmpeg is required for video thumbnail generation (optional).
Without ffmpeg, thumbnails are generated on the app side instead.
