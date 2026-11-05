#!/usr/bin/env python3

import os
import pathlib
import re


version = os.environ["RELEASE_VERSION"]
root = pathlib.Path(".")

before_file = pathlib.Path(os.environ["RUNNER_TEMP"]) / "conda-before.txt"

before = set()
if before_file.exists():
    before = set(before_file.read_text().splitlines())

after = {
    p.name
    for p in root.glob("*.conda")
}

new = sorted(after - before)

if len(new) != 1:
    raise SystemExit(
        "Expected exactly one new .conda package from pixi publish; "
        f"found {len(new)}: {new}"
    )

package = pathlib.Path(new[0])

expected = re.compile(
    rf"^.+-{re.escape(version)}-[^-]+\.conda$"
)

if not expected.match(package.name):
    raise SystemExit(
        f"Built package has unexpected version:\n"
        f"  expected: {version}\n"
        f"  package:  {package.name}"
    )

print(f"Validated package: {package}")
print(f"Expected version:  {version}")

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    print(f"package={package}", file=f)
