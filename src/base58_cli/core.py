"""Core Base58 encoding and decoding logic for base58-cli.

Implements the Bitcoin Base58 alphabet (digits 0, capital O, capital I,
and lowercase l are excluded to avoid visual ambiguity) using plain
big-integer arithmetic, so no external base58 library is required.
"""
from __future__ import annotations

ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_INDEX = {char: i for i, char in enumerate(ALPHABET)}


def encode(data: bytes) -> str:
    """Encode raw bytes as a Base58 string.

    Each leading 0x00 byte in `data` is encoded as a leading '1' in the
    output, per the standard Base58 convention for preserving byte-length
    information that big-integer conversion alone would lose.
    """
    if not data:
        return ""

    n = int.from_bytes(data, "big")
    digits: list[str] = []
    while n > 0:
        n, remainder = divmod(n, 58)
        digits.append(ALPHABET[remainder])
    body = "".join(reversed(digits))

    n_leading_zeros = len(data) - len(data.lstrip(b"\x00"))
    return ALPHABET[0] * n_leading_zeros + body


def decode(text: str) -> bytes:
    """Decode a Base58 string back into raw bytes.

    Each leading '1' character is decoded as a leading 0x00 byte. Raises
    `ValueError` if `text` contains a character outside the Base58
    alphabet.
    """
    if not text:
        return b""

    n = 0
    for char in text:
        if char not in _INDEX:
            raise ValueError(f"invalid base58 character: {char!r}")
        n = n * 58 + _INDEX[char]

    body = n.to_bytes((n.bit_length() + 7) // 8, "big") if n > 0 else b""

    n_leading_ones = len(text) - len(text.lstrip(ALPHABET[0]))
    return b"\x00" * n_leading_ones + body
