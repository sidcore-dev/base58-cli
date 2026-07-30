import unittest

from base58_cli.core import decode, encode


class TestEncode(unittest.TestCase):
    def test_empty_bytes(self) -> None:
        self.assertEqual(encode(b""), "")

    def test_known_vector(self) -> None:
        self.assertEqual(encode(b"hello world"), "StV1DL6CwTryKyV")

    def test_single_leading_zero_byte(self) -> None:
        self.assertEqual(encode(b"\x00"), "1")

    def test_multiple_leading_zero_bytes(self) -> None:
        self.assertEqual(encode(b"\x00\x00"), "11")

    def test_leading_zeros_preserved_with_data(self) -> None:
        self.assertEqual(encode(b"\x00\x00hello"), "11Cn8eVZg")


class TestDecode(unittest.TestCase):
    def test_empty_string(self) -> None:
        self.assertEqual(decode(""), b"")

    def test_known_vector(self) -> None:
        self.assertEqual(decode("StV1DL6CwTryKyV"), b"hello world")

    def test_invalid_character_raises(self) -> None:
        with self.assertRaises(ValueError):
            decode("0OIl")  # excluded from the Bitcoin alphabet

    def test_leading_ones_decode_to_zero_bytes(self) -> None:
        self.assertEqual(decode("11Cn8eVZg"), b"\x00\x00hello")


class TestRoundTrip(unittest.TestCase):
    def test_round_trip_arbitrary_bytes(self) -> None:
        for data in (b"", b"a", b"\x00", b"\x00\x01\x02\x03", b"binary safe \xff\xfe\x00", os_urandom_stub()):
            self.assertEqual(decode(encode(data)), data)

    def test_round_trip_preserves_leading_zero_count(self) -> None:
        data = b"\x00\x00\x00payload"
        self.assertEqual(decode(encode(data)), data)


def os_urandom_stub() -> bytes:
    # Deterministic "random-like" bytes, avoiding a dependency on os.urandom
    # for reproducible tests.
    return bytes((i * 37 + 5) % 256 for i in range(32))


if __name__ == "__main__":
    unittest.main()
