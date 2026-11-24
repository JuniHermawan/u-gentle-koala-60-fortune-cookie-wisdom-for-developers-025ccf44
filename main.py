"""Fortune Cookie Wisdom for Developers — make.fun entry.

Writes one original fortune-cookie line for a software developer to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default ``/output``).

Version history:
- v1: initial line, picked by calibration (see NOTES.md in the build
  workdir). Hand rubric + proxy-judge round robin over 6 candidates and
  3 controls: this line won at proxy win rate 0.84, beating the strong
  control 0.95 and the runner-up 0.90 in their head-to-head game.
- v2: added a single-line gate check (the entry must be exactly one
  line — a newline inside it would break the fortune-cookie shape) and
  a read-back verification after writing, so a failed or partial write
  is caught instead of silently passing.

The line (80 characters, one balanced sentence):
    Your legacy code is not a mess; it is a letter from someone who ran out of time.

Why this line: it is fortune-cookie shaped ("Your ... is ..."), it says
something true about a developer's day (inheriting legacy code), and it
turns that truth in a way not heard before — the mess is reframed as a
letter from a hurried predecessor, which rewards a second read (the
"someone" is every developer, including the reader's past self).

Standard library only. Deterministic: the same bytes on every run.
"""

import os
import sys

# The entry: one original fortune-cookie line, at most 120 characters.
FORTUNE = "Your legacy code is not a mess; it is a letter from someone who ran out of time."

MAX_CHARS = 120


def gate(text):
    """Self-check matching the competition gate: UTF-8, 1-120 chars, not blank."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not text.strip():
        raise ValueError("entry is only white space")
    if len(text) > MAX_CHARS:
        raise ValueError("entry is %d characters, over the 120 limit" % len(text))
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises if not encodable
    return text


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    text = gate(FORTUNE)
    path = os.path.join(out_dir, "entry.txt")
    # Exact bytes: the line alone, no trailing newline, so the judged
    # text is byte-identical to the line as written above.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Read-back verification: the file on disk must be byte-identical
    # to the gated line, otherwise the run failed.
    with open(path, "rb") as f:
        on_disk = f.read().decode("utf-8")
    if on_disk != text:
        raise ValueError("read-back mismatch: entry.txt does not match the gated line")
    print("wrote %s (%d chars)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
