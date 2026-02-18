#!/usr/bin/env python3
"""Update StillMotion Server download pages with new version/size/URL info."""

import argparse
import json
import os
import re


# (platform, filename_template, note_ja, note_en)
# {version} in filename_template is replaced with the actual version
FILE_DEFS = [
    ("macOS (Apple Silicon)", "StillMotion-Server-{version}.dmg",
     "推奨。DMGインストーラー", "Recommended. DMG installer"),
    ("macOS (Apple Silicon)", "stillmotion-server-darwin-arm64",
     "CLI バイナリ", "CLI binary"),
    ("macOS (Intel)", "stillmotion-server-darwin-amd64",
     "CLI バイナリ", "CLI binary"),
    ("Linux (x86_64)", "stillmotion-server-linux-amd64",
     "CLI バイナリ", "CLI binary"),
    ("Linux (ARM64)", "stillmotion-server-linux-arm64",
     "Raspberry Pi 等", "Raspberry Pi, etc."),
    ("Windows (x86_64)", "stillmotion-server-windows-amd64.exe",
     "ダブルクリックで起動", "Double-click to run"),
    ("Windows (ARM64)", "stillmotion-server-windows-arm64.exe",
     "ダブルクリックで起動", "Double-click to run"),
]


def yaml_quote(s):
    """Quote a string for YAML output."""
    return f'"{s}"'


def build_front_matter(title, description, version, tag, repo, sizes, lang):
    """Build YAML front matter string."""
    base_url = f"https://github.com/{repo}/releases/download/{tag}"

    lines = [
        "---",
        f"title: {yaml_quote(title)}",
        f"description: {yaml_quote(description)}",
        "download:",
        f"  appSlug: {yaml_quote('stillmotion')}",
        "  releases:",
        f"    - version: {yaml_quote(version)}",
        f"      githubRelease: {yaml_quote(tag)}",
        "      files:",
    ]

    for platform, fn_template, note_ja, note_en in FILE_DEFS:
        filename = fn_template.format(version=version)
        note = note_ja if lang == "ja" else note_en
        size = sizes.get(filename, "")
        url = f"{base_url}/{filename}"
        lines.extend([
            f"        - platform: {yaml_quote(platform)}",
            f"          filename: {yaml_quote(filename)}",
            f"          url: {yaml_quote(url)}",
            f"          size: {yaml_quote(size)}",
            f"          note: {yaml_quote(note)}",
        ])

    lines.append("---")
    return "\n".join(lines)


def update_file(filepath, version, tag, repo, sizes, lang):
    """Update a single download page file."""
    with open(filepath, "r") as f:
        content = f.read()

    # Split on "---" to get front matter and body
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"Invalid front matter in {filepath}")

    body = parts[2]  # Everything after second ---

    # Extract title and description from existing front matter
    fm = parts[1]
    title_match = re.search(r'title:\s*"(.+?)"', fm)
    desc_match = re.search(r'description:\s*"(.+?)"', fm)

    title = title_match.group(1) if title_match else ""
    description = desc_match.group(1) if desc_match else ""

    new_front_matter = build_front_matter(
        title, description, version, tag, repo, sizes, lang
    )

    with open(filepath, "w") as f:
        f.write(new_front_matter + body)

    print(f"  Updated: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="Update StillMotion Server download pages"
    )
    parser.add_argument("--version", required=True,
                        help="Version number (e.g. 1.1)")
    parser.add_argument("--sizes", required=True,
                        help="JSON object of filename:size mappings")
    parser.add_argument("--repo", required=True,
                        help="GitHub repo (e.g. frkake/yohaku)")
    parser.add_argument("--tag", required=True,
                        help="Release tag (e.g. stillmotion-server-v1.1)")
    args = parser.parse_args()

    sizes = json.loads(args.sizes)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    for lang in ("ja", "en"):
        filepath = os.path.join(
            project_root, "content", lang,
            "downloads", "stillmotion-server", "index.md"
        )
        update_file(filepath, args.version, args.tag, args.repo, sizes, lang)

    print(f"Download pages updated for v{args.version}")


if __name__ == "__main__":
    main()
