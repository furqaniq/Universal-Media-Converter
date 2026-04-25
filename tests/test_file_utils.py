"""Unit tests for file_utils module."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils.file_utils import format_file_size, sanitize_filename, get_unique_filename, detect_file_category


class TestFileUtils(unittest.TestCase):
    def test_format_file_size(self):
        self.assertEqual(format_file_size(0), "0 B")
        self.assertEqual(format_file_size(512), "512.0 B")
        self.assertEqual(format_file_size(1024), "1.0 KB")
        self.assertEqual(format_file_size(1024 * 1024), "1.0 MB")
        self.assertEqual(format_file_size(1024 * 1024 * 1024), "1.0 GB")

    def test_sanitize_filename(self):
        self.assertEqual(sanitize_filename("test<file>.txt"), "test_file_.txt")
        self.assertEqual(sanitize_filename("hello:world.pdf"), "hello_world.pdf")
        self.assertEqual(sanitize_filename("normal.png"), "normal.png")

    def test_get_unique_filename(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # First call should return original
            result1 = get_unique_filename(tmpdir, "test.txt")
            self.assertTrue(result1.endswith("test.txt"))
            open(result1, "w").close()

            # Second call should append (1)
            result2 = get_unique_filename(tmpdir, "test.txt")
            self.assertTrue(result2.endswith("test (1).txt"))

    def test_detect_file_category(self):
        self.assertEqual(detect_file_category("photo.jpg"), "image")
        self.assertEqual(detect_file_category("video.mp4"), "video")
        self.assertEqual(detect_file_category("doc.pdf"), "document")
        self.assertEqual(detect_file_category("unknown.xyz"), "unknown")


if __name__ == "__main__":
    unittest.main()
