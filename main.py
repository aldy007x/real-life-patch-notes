#!/usr/bin/env python3
"""Real Life Patch Notes: The Comedy Changelog — make.fun bounty entry.

Writes exactly one comedy patch-note line to $MAKEFUN_OUTPUT_DIR/entry.txt.
Deterministic, stdlib only, no network.
"""

import hashlib
import os
import sys

ENTRY = "v2.4.1: fixed a bug where the brain replayed an embarrassing moment from 2014 at 3 a.m. instead of sleeping."

MAX_CHARS = 160


def main() -> int:
    # Self-check: the entry must be exactly one non-blank line of 1-160 chars.
    text = ENTRY.strip()
    if not text:
        print("error: entry is blank", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: entry must be exactly one line", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= MAX_CHARS:
        print(
            f"error: entry is {len(text)} chars, must be 1-{MAX_CHARS}",
            file=sys.stderr,
        )
        return 1
    if not text.startswith("v"):
        print("error: entry must start with a version number", file=sys.stderr)
        return 1
    # UTF-8 round-trip: the line must survive a strict encode/decode unchanged.
    if text.encode("utf-8").decode("utf-8") != text:
        print("error: entry is not clean UTF-8 text", file=sys.stderr)
        return 1

    data = (text + "\n").encode("utf-8")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)
    print(f"wrote {path} ({len(text)} chars, sha256 {hashlib.sha256(data).hexdigest()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
