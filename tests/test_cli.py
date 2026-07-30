import io
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from base58_cli.cli import main


class FakeBuffer(io.BytesIO):
    """A BytesIO that survives being wrapped as sys.stdin.buffer / sys.stdout.buffer."""


class TestCli(unittest.TestCase):
    def _run(self, argv: list[str], stdin_bytes: bytes = b"") -> tuple[int, bytes]:
        fake_stdin = FakeBuffer(stdin_bytes)
        fake_stdout = FakeBuffer()
        with patch("sys.stdin") as stdin_mock, patch("sys.stdout") as stdout_mock:
            stdin_mock.buffer = fake_stdin
            stdout_mock.buffer = fake_stdout
            stdout_mock.write = lambda s: fake_stdout.write(s.encode("utf-8"))
            code = main(argv)
        return code, fake_stdout.getvalue()

    def test_encodes_stdin_to_stdout(self) -> None:
        code, out = self._run([], stdin_bytes=b"hello world")
        self.assertEqual(code, 0)
        self.assertEqual(out.decode().strip(), "StV1DL6CwTryKyV")

    def test_decodes_stdin_to_stdout(self) -> None:
        code, out = self._run(["--decode"], stdin_bytes=b"StV1DL6CwTryKyV\n")
        self.assertEqual(code, 0)
        self.assertEqual(out, b"hello world")

    def test_reads_from_file(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.bin"
            path.write_bytes(b"hello world")
            code, out = self._run(["--file", str(path)])
            self.assertEqual(code, 0)
            self.assertEqual(out.decode().strip(), "StV1DL6CwTryKyV")

    def test_decode_invalid_character_errors(self) -> None:
        err = io.StringIO()
        with redirect_stderr(err):
            code, _ = self._run(["--decode"], stdin_bytes=b"not0valid\n")
        self.assertEqual(code, 1)
        self.assertIn("invalid base58 character", err.getvalue())

    def test_missing_file_returns_exit_code_two(self) -> None:
        err = io.StringIO()
        with redirect_stderr(err):
            code = main(["--file", "/no/such/file"])
        self.assertEqual(code, 2)
        self.assertIn("could not read", err.getvalue())


if __name__ == "__main__":
    unittest.main()
