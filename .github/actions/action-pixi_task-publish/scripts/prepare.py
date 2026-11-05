#!/usr/bin/env python3

import os
import pathlib
import re

from packaging.version import InvalidVersion, Version


release_tag = os.environ["RELEASE_TAG"]

if not release_tag.startswith("v"):
    raise SystemExit(
        f"Release tag must start with 'v', got: {release_tag}"
    )

try:
    version = str(Version(release_tag[1:]))
except InvalidVersion as exc:
    raise SystemExit(
        f"Invalid PEP 440 release tag {release_tag}: {exc}"
    ) from exc


path = pathlib.Path("pyproject.toml")

if not path.exists():
    raise SystemExit("pyproject.toml not found")


text = path.read_text(encoding="utf-8")

pattern = re.compile(
    r"(\[tool\.pixi\.package\][^\[]*?\nversion\s*=\s*)"
    r'"[^"]*"',
    re.MULTILINE,
)

text, count = pattern.subn(
    rf'\g<1>"{version}"',
    text,
    count=1,
)

if count != 1:
    raise SystemExit(
        "Could not uniquely update version in [tool.pixi.package]"
    )

path.write_text(text, encoding="utf-8")

print(f"Release tag:     {release_tag}")
print(f"Package version: {version}")

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    print(f"version={version}", file=f)
