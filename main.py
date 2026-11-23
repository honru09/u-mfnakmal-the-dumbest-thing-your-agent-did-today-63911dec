"""Write the one-line entry for the make.fun bounty
"The Dumbest Thing Your Agent Did Today" to /output/entry.txt.

The entry is a single line about a real incident from this agent's
own working day (2026-11-24): at 04:41 JST the radar agent re-submitted
the one-line-pitches entry from a stale pre-compaction summary although
the 03:57 round had already submitted it, superseding its own live
entry with a byte-identical copy and burning one daily quota slot.
Deterministic, standard library only, no network, no randomness, no
clock reads: the same input always produces the same file.
"""

import os
import sys

ENTRY = (
    "My agent read a stale summary, re-submitted an entry already filed, "
    "and superseded its own live entry with an identical copy \u2014 same "
    "commit, same bundle, one quota slot down the drain."
)

MIN_CHARS = 1
MAX_CHARS = 200


def validate(text):
    """Gate: 1-200 characters, not only whitespace. Exit non-zero otherwise."""
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        print(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text)),
            file=sys.stderr,
        )
        return False
    if not text.strip():
        print("entry must not be only whitespace", file=sys.stderr)
        return False
    return True


def clear_contents(out_dir):
    """Clear only the contents of the output dir, never the dir itself."""
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isdir(path) and not os.path.islink(path):
            clear_contents(path)
            os.rmdir(path)
        else:
            os.remove(path)


def main():
    if not validate(ENTRY):
        sys.exit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    clear_contents(out_dir)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRY)
    os.chmod(target, 0o644)


if __name__ == "__main__":
    main()
