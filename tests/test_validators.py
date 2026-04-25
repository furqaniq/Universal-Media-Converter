"""Unit tests for validators module."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils.validators import validate_file, validate_output_format, validate_conversion_pair


class TestValidators(unittest.TestCase):
    def test_validate_file_not_exists(self):
        valid, msg = validate_file("/nonexistent/file.jpg", "image")
        self.assertFalse(valid)
        self.assertIn("does not exist", msg)

    def test_validate_file_invalid_type(self):
        with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as tmp:
            tmp.write(b"test")
            path = tmp.name
        try:
            valid, msg = validate_file(path, "image")
            self.assertFalse(valid)
            self.assertIn("Unsupported", msg)
        finally:
            os.unlink(path)

    def test_validate_output_format(self):
        self.assertTrue(validate_output_format("png", "image")[0])
        self.assertFalse(validate_output_format("xyz", "image")[0])

    def test_validate_conversion_pair(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp.write(b"test")
            path = tmp.name
        try:
            valid, msg = validate_conversion_pair(path, "jpg", "image")
            self.assertTrue(valid)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
