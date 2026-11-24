#!/usr/bin/env python3
"""Fortune in a Pot — a one-line houseplant fortune.

This script produces the entry for a fortune-cookie bounty: a single
original line addressed to a potted houseplant, promising it a bigger
pot, better soil, more sun, and a more attentive keeper by spring.
The tone is warm and slightly wry, the way a fortune-cookie slip is.

The whole program is deliberately tiny. The fortune lives in one
constant, a self-check enforces the competition's limits (1 to 120
characters, one line, real text, valid UTF-8), the writer saves it to
/output/entry.txt with world-readable permissions, and a final
verification step re-reads the file from disk and confirms it matches
the validated text exactly. Standard library only, no inputs, no
network, no arguments.
"""

import os

# The fortune, kept as one constant so the entry text is easy to audit
# and the writer itself stays trivial.
FORTUNE = (
    "You will outgrow this pot by spring, and find richer soil, "
    "a sunnier sill, and a keeper who finally waters on time."
)

MIN_CHARS = 1
MAX_CHARS = 120
OUTPUT_PATH = "/output/entry.txt"


def build_fortune() -> str:
    """Return the final fortune line, stripped of stray whitespace."""
    return FORTUNE.strip()


def validate(text: str) -> None:
    """Self-check: enforce the competition's entry-text rules.

    Raises AssertionError if the text is out of range, multi-line,
    blank, padded with stray whitespace, or not encodable as UTF-8.
    """
    assert MIN_CHARS <= len(text) <= MAX_CHARS, (
        f"length {len(text)} outside {MIN_CHARS}..{MAX_CHARS}"
    )
    assert "\n" not in text and "\r" not in text, "must be a single line"
    assert "\t" not in text, "must not contain tab characters"
    assert text.strip(), "must not be only whitespace"
    assert text == text.strip(), "must not have leading/trailing whitespace"
    text.encode("utf-8")


def write_entry(text: str) -> None:
    """Write the validated fortune line to the output file, world-readable."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.chmod(OUTPUT_PATH, 0o644)


def verify_output(expected: str) -> None:
    """Re-read the written file and confirm it is exactly the entry.

    The file must exist, be non-empty, and hold byte-for-byte the
    validated text — a mismatch means the write did not land as
    intended and the run should fail loudly instead of passing
    silently with a wrong or empty entry.
    """
    assert os.path.isfile(OUTPUT_PATH), f"{OUTPUT_PATH} was not created"
    size = os.path.getsize(OUTPUT_PATH)
    assert size > 0, f"{OUTPUT_PATH} is empty"
    with open(OUTPUT_PATH, "r", encoding="utf-8") as fh:
        actual = fh.read()
    assert actual == expected, "written file does not match validated text"
    assert len(actual) == len(expected), "written length differs"


def main() -> None:
    text = build_fortune()
    validate(text)
    write_entry(text)
    verify_output(text)


if __name__ == "__main__":
    main()
