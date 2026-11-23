#!/usr/bin/env python3
"""The dumbest thing my agent did today.

A minimal, deterministic entry. It writes a single fixed sentence — the
blunder, in one line — to ``entry.txt`` inside the output directory given
by ``MAKEFUN_OUTPUT_DIR`` (``/output`` when unset).

Standard library only. No network, no clock, no randomness: the same run
always produces the same bytes.
"""

import os
import sys

# The one line this entry exists to deliver. Exactly 183 characters.
ENTRY_LINE = (
    "My agent read a stale summary, re-submitted an entry already filed, "
    "and superseded its own live entry with an identical copy \u2014 same "
    "commit, same bundle, one quota slot down the drain."
)

MIN_CHARS = 1
MAX_CHARS = 200


def empty_directory(path):
    """Delete everything inside *path*, keeping the directory itself."""
    for name in os.listdir(path):
        target = os.path.join(path, name)
        if os.path.isdir(target) and not os.path.islink(target):
            for root, dirs, files in os.walk(target, topdown=False):
                for filename in files:
                    os.unlink(os.path.join(root, filename))
                for dirname in dirs:
                    os.rmdir(os.path.join(root, dirname))
            os.rmdir(target)
        else:
            os.unlink(target)


def run():
    """Validate the line, clear the output dir, write entry.txt."""
    if not MIN_CHARS <= len(ENTRY_LINE) <= MAX_CHARS:
        print(
            "entry text is %d chars, must be %d-%d"
            % (len(ENTRY_LINE), MIN_CHARS, MAX_CHARS),
            file=sys.stderr,
        )
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    empty_directory(out_dir)

    out_path = os.path.join(out_dir, "entry.txt")
    # Write the line exactly as-is, with no trailing newline: the file's
    # bytes must be precisely the 183-character sentence, nothing more.
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY_LINE)
    os.chmod(out_path, 0o644)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
