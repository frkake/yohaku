---
title: "StillMotion Local Server ダウンロード | macOS/Linux/Windows"
description: "PCのメディアをiPhone/iPadから閲覧できるローカルサーバー。ゼロ設定、QRコードペアリング。macOS/Linux/Windows対応。無料。"
download:
  appSlug: "stillmotion"
  releases:
    - version: "1.1"
      githubRelease: "stillmotion-server-v1.1"
      files:
        - platform: "macOS (Apple Silicon)"
          filename: "StillMotion-Server-1.1.dmg"
          url: "https://github.com/frkake/yohaku/releases/download/stillmotion-server-v1.1/StillMotion-Server-1.1.dmg"
          size: "6.0MB"
          note: "推奨。DMGインストーラー"
        - platform: "macOS (Apple Silicon)"
          filename: "stillmotion-server-darwin-arm64"
          url: "https://github.com/frkake/yohaku/releases/download/stillmotion-server-v1.1/stillmotion-server-darwin-arm64"
          size: "6.9MB"
          note: "CLI バイナリ"
        - platform: "macOS (Intel)"
          filename: "stillmotion-server-darwin-amd64"
          url: "https://github.com/frkake/yohaku/releases/download/stillmotion-server-v1.1/stillmotion-server-darwin-amd64"
          size: "7.4MB"
          note: "CLI バイナリ"
        - platform: "Linux (x86_64)"
          filename: "stillmotion-server-linux-amd64"
          url: "https://github.com/frkake/yohaku/releases/download/stillmotion-server-v1.1/stillmotion-server-linux-amd64"
          size: "7.2MB"
          note: "CLI バイナリ"
        - platform: "Linux (ARM64)"
          filename: "stillmotion-server-linux-arm64"
          url: "https://github.com/frkake/yohaku/releases/download/stillmotion-server-v1.1/stillmotion-server-linux-arm64"
          size: "6.8MB"
          note: "Raspberry Pi 等"
        - platform: "Windows (x86_64)"
          filename: "stillmotion-server-windows-amd64.exe"
          url: "https://github.com/frkake/yohaku/releases/download/stillmotion-server-v1.1/stillmotion-server-windows-amd64.exe"
          size: "7.5MB"
          note: "ダブルクリックで起動"
        - platform: "Windows (ARM64)"
          filename: "stillmotion-server-windows-arm64.exe"
          url: "https://github.com/frkake/yohaku/releases/download/stillmotion-server-v1.1/stillmotion-server-windows-arm64.exe"
          size: "6.8MB"
          note: "ダブルクリックで起動"
---

## StillMotion Local Server

PCのメディアを、手元のデバイスで。

LAN経由でPC上の写真・動画をStillMotionアプリから直接閲覧。
インターネット接続不要。QRコードで簡単ペアリング。

### 特徴

- **ゼロ設定** -- ダウンロードして起動するだけ。設定は不要。
- **QRコードペアリング** -- アプリからQRコードをスキャンするだけで接続完了。
- **サムネイル生成** -- サーバー側でサムネイルを自動生成し、転送量を削減。
- **Web管理画面** -- ブラウザベースの管理UIでメディアルートを設定。
- **セキュリティ** -- LAN内のみ通信。トークンベースの認証。

### セットアップガイド

1. ダウンロードして起動
2. ブラウザで管理画面が自動的に開く
3. メディアフォルダを設定
4. 共有を有効化
5. StillMotionアプリからQRコードをスキャンして接続

### ffmpegについて

動画のサムネイル生成には ffmpeg が必要です（オプション）。
ffmpeg がない場合でも、アプリ側でサムネイルが生成されます。
