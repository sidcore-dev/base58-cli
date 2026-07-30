"""Command-line entry point for base58-cli."""
from __future__ import annotations

import argparse
import sys

from .core import decode, encode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="base58-cli",
        description="Encode or decode Base58 (Bitcoin alphabet), binary-safe.",
    )
    parser.add_argument(
        "--file", default=None, help="Path to read input from (default: stdin)"
    )
    parser.add_argument(
        "--decode", action="store_true", help="Decode Base58 text back into raw bytes"
    )
    return parser


def _read_input(path: str | None, binary: bool) -> bytes:
    if path is not None:
        with open(path, "rb") as fh:
            return fh.read()
    return sys.stdin.buffer.read()


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        raw = _read_input(args.file, binary=True)
    except OSError as exc:
        print(f"base58-cli: error: could not read input: {exc}", file=sys.stderr)
        return 2

    if args.decode:
        try:
            text = raw.decode("ascii").strip()
        except UnicodeDecodeError:
            print("base58-cli: error: input is not valid ASCII Base58 text", file=sys.stderr)
            return 1
        try:
            data = decode(text)
        except ValueError as exc:
            print(f"base58-cli: error: {exc}", file=sys.stderr)
            return 1
        sys.stdout.buffer.write(data)
    else:
        sys.stdout.write(encode(raw) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
