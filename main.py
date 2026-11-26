#!/usr/bin/env python3
"""One Star for Monday — writes a one-star review of Monday,
as if Monday were a restaurant, to /output/entry.txt.

The review is a single line of plain text, at most 25 words,
and 1-180 characters, per the competition gate.
"""

import os
import sys

REVIEW = (
    "Waited 45 minutes, server brought the weekend's leftovers cold, "
    "then charged me a full week. One star. Never coming back Monday."
)

MAX_WORDS = 25
MAX_CHARS = 180


def validate_review(text):
    """Check the review against the competition gate before writing."""
    if not text or not text.strip():
        raise ValueError("review is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("review must be a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("review contains a control character")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("review is not valid UTF-8 text: %s" % exc)
    if len(text) > MAX_CHARS:
        raise ValueError(
            "review is %d characters, over the %d limit"
            % (len(text), MAX_CHARS)
        )
    words = text.split()
    if len(words) > MAX_WORDS:
        raise ValueError(
            "review is %d words, over the %d limit" % (len(words), MAX_WORDS)
        )
    return len(words), len(text)


def main():
    words, chars = validate_review(REVIEW)
    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(REVIEW)
    # Read it back and confirm what landed is exactly what we validated.
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != REVIEW:
        raise ValueError("round-trip check failed: file differs from review")
    validate_review(written)
    print("wrote %d words, %d characters to %s" % (words, chars, out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
