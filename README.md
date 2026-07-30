# base58-cli

A small, dependency-free command-line tool that encodes and decodes
Base58 using the Bitcoin alphabet (no `0`, `O`, `I`, or `l`).

## Why

Base58 shows up in Bitcoin addresses, IPFS CIDs, and short-URL-style
identifiers because it avoids visually ambiguous characters. Most
implementations pull in a small external library for something that's
really just big-integer division. `base58-cli` implements it directly
with Python's arbitrary-precision integers — no dependency required —
and is binary-safe, correctly preserving leading zero bytes.

## Install

```bash
pip install .
```

This installs a `base58-cli` command on your PATH.

## Usage

```bash
echo -n "hello world" | base58-cli
```

```
StV1DL6CwTryKyV
```

```bash
echo -n "StV1DL6CwTryKyV" | base58-cli --decode
```

```
hello world
```

Read from a file instead of stdin:

```bash
base58-cli --file image.png > image.b58
base58-cli --decode --file image.b58 > image.png
```

Leading zero bytes round-trip correctly, per the standard Base58
convention (each leading `0x00` byte becomes a leading `1` character):

```bash
printf '\x00\x00hello' | base58-cli
```

```
11Cn8eVZg
```

### Options

| Flag         | Description                                    |
|--------------|---------------------------------------------------|
| `--file PATH`| Read input from a file instead of stdin           |
| `--decode`   | Decode Base58 text back into raw bytes             |

### Exit codes

- `0` — success
- `1` — decode input contained a character outside the Base58 alphabet
- `2` — the input file couldn't be read

## Development

```bash
pip install -e .
python -m unittest discover -s tests -v
```

## License

All rights reserved. This code is public for viewing and reference only —
no license is granted to use, copy, modify, or redistribute it. See
[LICENSE](LICENSE) for details.
