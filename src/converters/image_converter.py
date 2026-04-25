"""Image conversion backend using Pillow."""

import os
import threading
from PIL import Image

from config import OUTPUTS_DIR
from utils.file_utils import get_unique_filename, get_file_extension


class ImageConverter:
    """Handles image format conversion, resize, and quality settings."""

    def __init__(self, progress_callback=None, completion_callback=None):
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback
        self._cancelled = False

    def cancel(self):
        """Signal cancellation of ongoing conversions."""
        self._cancelled = True

    def convert(
        self,
        input_path,
        output_format,
        output_dir=None,
        width=None,
        height=None,
        quality=95,
        preserve_transparency=True,
    ):
        """Convert a single image file.

        Returns output path on success, raises Exception on failure.
        """
        if self._cancelled:
            raise Exception("Conversion cancelled.")

        output_dir = output_dir or str(OUTPUTS_DIR)
        os.makedirs(output_dir, exist_ok=True)

        ext = output_format.lower()
        if ext == "jpg":
            ext = "jpeg"

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_name = f"{base_name}.{ext}"
        output_path = get_unique_filename(output_dir, output_name)

        with Image.open(input_path) as img:
            # Convert mode if needed
            if ext == "jpeg" and img.mode in ("RGBA", "P"):
                if preserve_transparency:
                    # Create white background for JPEG
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == "P":
                        img = img.convert("RGBA")
                    background.paste(img, mask=img.split()[-1])
                    img = background
                else:
                    img = img.convert("RGB")
            elif img.mode == "RGBA" and ext not in ("png", "webp", "tiff"):
                img = img.convert("RGB")
            elif img.mode == "P" and ext in ("png", "webp", "tiff") and preserve_transparency:
                img = img.convert("RGBA")

            # Resize if dimensions provided
            if width or height:
                original_width, original_height = img.size
                new_width = width or original_width
                new_height = height or original_height
                img = img.resize((new_width, new_height), Image.LANCZOS)

            # Save with appropriate options
            save_kwargs = {}
            if ext in ("jpeg", "webp"):
                save_kwargs["quality"] = quality
                save_kwargs["optimize"] = True
            if ext == "png" and img.mode == "RGBA":
                save_kwargs["optimize"] = True

            img.save(output_path, format=ext.upper(), **save_kwargs)

        return output_path

    def convert_batch(
        self,
        file_paths,
        output_format,
        output_dir=None,
        width=None,
        height=None,
        quality=95,
        preserve_transparency=True,
    ):
        """Convert multiple images sequentially in a background thread."""

        def _run():
            total = len(file_paths)
            results = []
            for i, path in enumerate(file_paths):
                if self._cancelled:
                    break
                try:
                    if self.progress_callback:
                        self.progress_callback(path, "processing", (i / total) * 100)

                    out = self.convert(
                        path,
                        output_format,
                        output_dir,
                        width,
                        height,
                        quality,
                        preserve_transparency,
                    )
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
