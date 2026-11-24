#!/usr/bin/env python3
"""Fortune in a Pot.

Writes one original fortune-cookie line for a houseplant to
/output/entry.txt. Standard library only.

The fortune is a single constant, validated by an explicit self-check
before writing: the gate wants UTF-8 text of 1 to 120 characters, a
single line, and more than whitespace. The output file is written with
a plain open() and chmod 0644 so the grader (a different user) can
read it.
"""

import os

# The fortune, kept as one constant so the entry text is easy to audit
# and the writer itself stays trivial.
FORTUNE = (
    "You will outgrow this pot by spring, and find richer soil, "
    "a sunnier sill, and a keeper who finally waters on time."
)

MAX_CHARS = 120
OUTPUT_PATH = "/output/entry.txt"


def build_fortune() -> str:
    """Return the final fortune line, stripped of stray whitespace."""
    return FORTUNE.strip()


def validate(text: str) -> None:
    """Self-check: enforce the competition's entry-text rules.

    Raises AssertionError if the text is out of range, multi-line,
    blank, or not encodable as UTF-8.
    """
    assert 1 <= len(text) <= MAX_CHARS, f"length {len(text)} out of range"
    assert "\n" not in text and "\r" not in text, "must be a single line"
    assert text.strip(), "must not be only whitespace"
    text.encode("utf-8")


def write_entry(text: str) -> None:
    """Write the validated fortune line to the output file, world-readable."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.chmod(OUTPUT_PATH, 0o644)


def main() -> None:
    text = build_fortune()
    validate(text)
    write_entry(text)


if __name__ == "__main__":
    main()
