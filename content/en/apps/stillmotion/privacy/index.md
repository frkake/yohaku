---
title: "Privacy Policy"
description: "StillMotion Privacy Policy"
type: "legal"
date: 2026-02-25
showDate: true
showReadingTime: false
---

## Introduction

This Privacy Policy describes how "StillMotion" ("the App"), developed by Takumi Iida, handles your data. This policy applies to all features and services provided by the App.

## Information We Collect

The App does not collect any personal information.

We may receive anonymized usage statistics through Apple's standard analytics (App Analytics), which includes app usage data and crash reports. The App does not track users across other apps or websites (`NSPrivacyTracking = false`).

## Third-Party Service Integrations

The App provides optional integrations with the following third-party services. All integrations are read-only and used solely for browsing and viewing media within the App. Some integrations listed below may be pending deployment and not yet available in the current release.

### Google Drive

- **Scope:** `drive.readonly` (read-only access)
- **Purpose:** Listing files and folders, downloading and viewing media
- **API:** Google Drive API v3
- **Authentication:** OAuth 2.0 with PKCE (SHA-256)
- The App does not modify, delete, or create any files on your Google Drive.

### Google Photos

- **Scope:** `photospicker.mediaitems.readonly` (read-only access)
- **Purpose:** Viewing photos selected by the user
- **API:** Google Photos Picker API v1
- **Authentication:** OAuth 2.0 with PKCE (SHA-256)
- The App does not modify, delete, or upload any photos to your Google Photos.

### Dropbox

- **Access:** Read-only (folder listing, temporary download links, thumbnail retrieval)
- **API:** Dropbox API v2 (`list_folder`, `get_temporary_link`, `get_thumbnail_v2`)
- **Authentication:** OAuth 2.0 with PKCE (SHA-256)
- The App does not write to, delete from, or modify any content in your Dropbox.

### SSH/SFTP

- Read-only connection to user-configured servers
- Authentication credentials are stored encrypted in Apple Keychain

### Local Server

- Operates exclusively within your local network (LAN)
- No data is sent or received over the internet

### Photos App & Files App

- Accessed through standard OS-provided access mechanisms

## How We Use Your Data

- Data accessed through third-party services is used solely for providing media browsing and viewing functionality within the App.
- We do not use your data for advertising, marketing, or analytics purposes.
- We do not provide your data to any third party.

## Data Storage and Security

- **OAuth tokens:** Stored encrypted in Apple Keychain
- **Media cache:** Stored in the device's cache directory (TTL: 24 hours; thumbnails: 3.5 hours)
- **Settings:** Stored locally in UserDefaults
- **No data is ever sent to the developer's servers.**
- All API communications are encrypted via HTTPS.

## Data Retention and Deletion

- Cached data is automatically deleted after its TTL expires and is size-limited using LRU eviction.
- You can manually clear the cache within the App.
- Logging out of each service immediately deletes its tokens from Keychain.
- Uninstalling the App deletes all associated data from your device.
- You can also revoke the App's access to your Google account at any time at [https://myaccount.google.com/permissions](https://myaccount.google.com/permissions).
- You can also revoke the App's access to your Dropbox account at any time at [https://www.dropbox.com/account/connected_apps](https://www.dropbox.com/account/connected_apps).

## Google API Services — Limited Use Disclosure

StillMotion's use and transfer to any other app of information received from Google APIs will adhere to the [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy), including the Limited Use requirements.

Specifically, the App:

1. **Only uses Google API data to provide media browsing and viewing functionality** — the core functionality of the App as described in this policy.
2. **Does not transfer Google API data to third parties**, except as necessary to provide or improve the App's functionality, with user consent, for security purposes, or to comply with applicable laws.
3. **Does not use Google API data for advertising purposes.** The App does not serve ads, and Google API data is never used to serve, target, or personalize advertisements.
4. **Does not allow humans to read Google API data**, unless with the user's affirmative consent, for security purposes, to comply with applicable laws, or when data is aggregated and anonymized for internal operations.

## Data Sharing

- We do not share any user data with third parties.
- The App does not include any advertising SDKs or third-party analytics SDKs.

## Children's Privacy

The App does not knowingly collect personal information from children under 13. Since the App does not collect any personal information from any user, no special provisions are required.

## Changes to This Policy

We may update this policy as needed. Significant changes will be posted on this page.

## Contact Us

If you have any questions about this Privacy Policy, please contact us:

- **Email:** takumifujinolab@gmail.com
- **Website:** [https://less-is-more.ai/](https://less-is-more.ai/)
- **Developer:** Takumi Iida
