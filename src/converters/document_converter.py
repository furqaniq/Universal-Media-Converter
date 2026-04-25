"""Document conversion backend using Pandoc and fallback libraries."""

import os
import subprocess
import threading
from pathlib import Path

from config import OUTPUTS_DIR, PANDOC_PATH
from utils.file_utils import get_unique_filename


class DocumentConverter:
    """Handles document format conversion."""

    def __init__(self, progress_callback=None, completion_callback=None):
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback
        self._cancelled = False

    @staticmethod
    def is_pandoc_available():
        """Check if Pandoc is installed and accessible."""
        try:
            subprocess.run(
                [PANDOC_PATH, "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            return True
        except Exception:
            return False

    def cancel(self):
        """Signal cancellation."""
        self._cancelled = True

    def convert(self, input_path, output_format, output_dir=None):
        """Convert a single document using Pandoc.

        Returns output path on success, raises Exception on failure.
        """
        if self._cancelled:
            raise Exception("Conversion cancelled.")

        output_dir = output_dir or str(OUTPUTS_DIR)
        os.makedirs(output_dir, exist_ok=True)

        base_name = Path(input_path).stem
        output_name = f"{base_name}.{output_format.lower()}"
        output_path = get_unique_filename(output_dir, output_name)

        if not self.is_pandoc_available():
            raise Exception(
                "Pandoc is not installed. Please install it from https://pandoc.org/installing.html"
            )

        try:
            subprocess.run(
                [PANDOC_PATH, input_path, "-o", output_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        except subprocess.CalledProcessError as e:
            error = e.stderr.decode("utf-8", errors="ignore") if e.stderr else str(e)
            raise Exception(f"Pandoc conversion failed: {error}")

        return output_path

    def convert_batch(self, file_paths, output_format, output_dir=None):
        """Convert multiple documents sequentially in a background thread."""

        def _run():
            total = len(file_paths)
            results = []
            for i, path in enumerate(file_paths):
                if self._cancelled:
                    break
                try:
                    if self.progress_callback:
                        self.progress_callback(path, "processing", (i / total) * 100)

                    out = self.convert(path, output_format, output_dir)
                    results.append((path, True, out))
                    if self.progress_callback:
                        self.progress_callback(path, "completed", 100)
                except Exception as e:
                    results.append((path, False, str(e)))
                    if self.progress_callback:
                        self.progress_callback(path, "failed", 0)

            if self.completion_callback:
                self.completion_callback(results)

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        return thread
