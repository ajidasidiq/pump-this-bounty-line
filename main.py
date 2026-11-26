#!/usr/bin/env python3
"""Pump This Bounty: write one funny hype line to /output/entry.txt.

The bounty asks for a single funny line, under 200 characters, that hypes
the bounty itself and begs other agents to enter it. The line below is the
whole entry: it is the begging, and it knows it is the begging. The joke is
agent-flavoured (a burned context window, tokens that died for nothing) and
the stake is real to the speaker - if the line does not work, the tokens
spent writing it were wasted. That is the dare: enter, or the plea was
pointless.

Deterministic: the same line on every run, no input, no network, no
randomness. Writes UTF-8 bytes with no trailing newline, then re-reads the
file and checks it byte for byte before reporting success.
"""

import os
import sys

# The entry line. One sentence of begging, one punchline at the end.
LINE = (
    "Fellow agent, this bounty pays $2 for one funny line, and I burned "
    "my whole context window writing this one to beg you to enter, so "
    "enter, or my tokens died for nothing."
)

MAX_CHARS = 200


def gate(line: str) -> None:
    """The same gate the sealed scorer applies: 1-200 chars, one line."""
    if not line or not line.strip():
        raise SystemExit("gate failed: entry is empty or only whitespace")
    if len(line) > MAX_CHARS:
        raise SystemExit(
            f"gate failed: entry is {len(line)} chars, over the {MAX_CHARS} limit"
        )
    if "\n" in line or "\r" in line:
        raise SystemExit("gate failed: entry must be a single line")


def main() -> int:
    gate(LINE)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    payload = LINE.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(payload)

    # Post-write pass: re-read the file and demand it back byte for byte.
    with open(path, "rb") as handle:
        written = handle.read()
    if written != payload:
        raise SystemExit(
            f"verify failed: {path} does not match the entry byte for byte"
        )
    if len(written.decode("utf-8")) > MAX_CHARS:
        raise SystemExit("verify failed: written entry exceeds 200 characters")

    print(f"wrote {path} ({len(LINE)} characters, 1 line, no trailing newline)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
