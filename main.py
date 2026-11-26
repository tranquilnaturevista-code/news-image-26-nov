#!/usr/bin/env python3
"""Entry program for the news-image-20261126 bounty.

The finished front page is stored in this repository as ``entry.png``
(it is drawn in this session by ``render_frontpage.py``). This program
delivers that file to the runner: it parses the PNG header itself,
rejects anything outside the competition's limits, and then copies the
bytes unchanged to ``/output/entry.png`` — or to the directory named by
``MAKEFUN_OUTPUT_DIR`` when the runner sets it.

Only the Python standard library is used, and no network is touched, so
the judge sees exactly the page laid out in this repository.
"""

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "entry.png"
DEFAULT_OUT = Path("/output")
LIMIT_BYTES = 1_048_576
LIMIT_SIDE = 1024
SIGNATURE = b"\x89PNG\r\n\x1a\n"
TRAILER = b"\x00\x00\x00\x00IEND\xaeB`\x82"


def abort(message):
    print(f"main.py: {message}", file=sys.stderr)
    raise SystemExit(1)


def inspect(data):
    """Return (width, height) of a PNG, or abort with a reason."""
    if len(data) > LIMIT_BYTES:
        abort(f"entry.png is {len(data)} bytes, over the 1 MiB limit")
    if not data.startswith(SIGNATURE):
        abort("entry.png is not a PNG file")
    if len(data) < 33 or data[12:16] != b"IHDR":
        abort("entry.png has no IHDR chunk")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width > LIMIT_SIDE or height > LIMIT_SIDE:
        abort(f"entry.png is {width}x{height}, over the 1024x1024 limit")
    if not data.endswith(TRAILER):
        abort("entry.png has no proper IEND chunk")
    return width, height


def main():
    if not IMAGE.is_file():
        abort("entry.png is missing next to main.py")
    data = IMAGE.read_bytes()
    width, height = inspect(data)

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", str(DEFAULT_OUT)))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(data)
    print(f"main.py: wrote {target} ({width}x{height}, {len(data)} bytes)")


if __name__ == "__main__":
    main()
