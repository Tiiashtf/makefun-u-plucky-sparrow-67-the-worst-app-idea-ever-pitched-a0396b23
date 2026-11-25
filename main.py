#!/usr/bin/env python3
"""The Worst App Idea Ever Pitched — SockSync.

Writes a single original one-sentence pitch of the worst, most useless
app imaginable to /output/entry.txt.
209 characters, one sentence, no trailing newline.
Deterministic, stdlib only, no network.

Run:  python3 main.py
"""

import os
import sys

PITCH = (
    "SockSync is the Bluetooth app that pairs your left sock with your right sock "
    "and pings your phone the instant one vanishes in the wash, because matching "
    "socks by eye was simply too much for one person to bear."
)

OUTPUT_DIR = "/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.txt")


def clear_contents(path):
    """Remove only the contents of path, never path itself.

    Best effort: a stale entry that cannot be removed (for example a
    root-owned subdirectory the grader left behind) must not fail the
    run — the gate only needs /output/entry.txt written correctly.
    """
    for name in os.listdir(path):
        target = os.path.join(path, name)
        try:
            if os.path.islink(target) or os.path.isfile(target):
                os.unlink(target)
            elif os.path.isdir(target):
                for root, dirs, files in os.walk(target, topdown=False):
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except OSError:
                            pass
                    for d in dirs:
                        link = os.path.join(root, d)
                        try:
                            if os.path.islink(link):
                                os.unlink(link)
                            else:
                                os.rmdir(link)
                        except OSError:
                            pass
                os.rmdir(target)
            else:
                os.unlink(target)
        except OSError:
            pass


def main():
    text = PITCH
    if not (1 <= len(text) <= 240):
        print(f"pitch is {len(text)} chars, must be 1-240", file=sys.stderr)
        return 1
    if not text.strip():
        print("pitch is blank", file=sys.stderr)
        return 1
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    clear_contents(OUTPUT_DIR)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"wrote {len(text)} chars to {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
