#!/usr/bin/env python3
"""Update StillMotion Server data file with new version/size info."""

import argparse
import json
import os


# (platform, filename_template, noteKey)
# {version} in filename_template is replaced with the actual version
FILE_DEFS = [
    ("macOS (Apple Silicon)", "StillMotion-Server-{version}.dmg",
     "note_dmg_installer"),
    ("macOS (Apple Silicon)", "stillmotion-server-darwin-arm64",
     "note_cli_binary"),
    ("macOS (Intel)", "stillmotion-server-darwin-amd64",
     "note_cli_binary"),
    ("Linux (x86_64)", "stillmotion-server-linux-amd64",
     "note_cli_binary"),
    ("Linux (ARM64)", "stillmotion-server-linux-arm64",
     "note_raspberry_pi"),
    ("Windows (x86_64)", "stillmotion-server-windows-amd64.exe",
     "note_doubleclick"),
    ("Windows (ARM64)", "stillmotion-server-windows-arm64.exe",
     "note_doubleclick"),
]


def yaml_quote(s):
    """Quote a string for YAML output."""
    return f'"{s}"'


def build_data_file(version, tag, repo, sizes):
    """Build YAML data file string."""
    lines = [
        "# CI-managed -- do not edit manually",
        f"appSlug: {yaml_quote('stillmotion')}",
        f"repo: {yaml_quote(repo)}",
        "releases:",
        f"  - version: {yaml_quote(version)}",
        f"    tag: {yaml_quote(tag)}",
        "    files:",
    ]

    for platform, fn_template, note_key in FILE_DEFS:
        filename = fn_template.format(version=version)
        size = sizes.get(filename, "")
        lines.extend([
            f"      - platform: {yaml_quote(platform)}",
            f"        filename: {yaml_quote(filename)}",
            f"        size: {yaml_quote(size)}",
            f"        noteKey: {yaml_quote(note_key)}",
        ])

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Update StillMotion Server data file"
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

    filepath = os.path.join(
        project_root, "data", "downloads", "stillmotion-server.yaml"
    )

    content = build_data_file(args.version, args.tag, args.repo, sizes)

    with open(filepath, "w") as f:
        f.write(content)

    print(f"  Updated: {filepath}")
    print(f"Data file updated for v{args.version}")


if __name__ == "__main__":
    main()
