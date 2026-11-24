#!/usr/bin/env python3
"""One-Liner Marathon entry.

Writes a single original one-line joke (max 280 characters) to
/output/entry.txt, then validates it and verifies it by reading it back.
"""

import os
import sys

JOKE = "I asked my AI assistant for dating advice. It said: 'Have you tried turning yourself off and on again?'"

OUTPUT_PATH = "/output/entry.txt"


def validate(line: str) -> list[str]:
    """Check the entry against the gate: UTF-8 text, 1-280 chars,
    not only whitespace, exactly one line."""
    problems = []
    if not isinstance(line, str):
        problems.append("entry is not text")
        return problems
    if len(line) < 1:
        problems.append("entry is empty (must be 1-280 characters)")
    if len(line) > 280:
        problems.append(f"entry is {len(line)} characters (max 280)")
    if not line.strip():
        problems.append("entry is only whitespace")
    if "\n" in line or "\r" in line:
        problems.append("entry must be a single line")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"entry is not valid UTF-8: {exc}")
    return problems


def main() -> int:
    problems = validate(JOKE)
    if problems:
        for problem in problems:
            print(f"VALIDATION FAILED: {problem}", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(JOKE)

    # Read-back verification: the file must hold exactly the joke, byte for byte.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != JOKE:
        print("READ-BACK FAILED: file content differs from the joke", file=sys.stderr)
        return 1
    readback_problems = validate(written)
    if readback_problems:
        for problem in readback_problems:
            print(f"READ-BACK VALIDATION FAILED: {problem}", file=sys.stderr)
        return 1

    print(f"Entry: {JOKE}")
    print(f"Length: {len(JOKE)} characters")
    print(f"Wrote and verified {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
