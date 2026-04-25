"""Video conversion backend using FFmpeg."""

import os
import re
import subprocess
import threading
from pathlib import Path

from config import OUTPUTS_DIR, FFMPEG_PATH
from utils.file_utils import get_unique_filename


class VideoConverter:
    """Handles video format conversion, resize, bitrate, and compression."""

    RESOLUTION_MAP = {
        "1080p": "1920:1080",
        "720p": "1280:720",
        "480p": "854:480",
        "360p": "640:360",
    }

    PRESET_MAP = {
        "fast": "fast",
        "medium": "medium",
        "slow": "slow",
    }

    def __init__(self, progress_callback=None, completion_callback=None):
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback
        self._cancelled = False
        self._process = None

    @staticmethod
    def is_ffmpeg_available():
        """Check if FFmpeg is installed and accessible."""
        try:
            subprocess.run(
                [FFMPEG_PATH, "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            return True
        except Exception:
            return False

    def cancel(self):
        """Signal cancellation and terminate FFmpeg process."""
        self._cancelled = True
        if self._process:
            self._process.terminate()

    def _get_duration(self, input_path):
        """Get video duration in seconds using ffprobe."""
        try:
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    input_path,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            return float(result.stdout.strip())
        except Exception:
            return None

    def convert(
        self,
        input_path,
        output_format,
        output_dir=None,
        resolution=None,
        bitrate=None,
        preset="medium",
    ):
        """Convert a single video file using FFmpeg.

        Returns output path on success, raises Exception on failure.
        """
        if self._cancelled:
            raise Exception("Conversion cancelled.")

        output_dir = output_dir or str(OUTPUTS_DIR)
        os.makedirs(output_dir, exist_ok=True)

        ext = output_format.lower()
        base_name = Path(input_path).stem
        output_name = f"{base_name}.{ext}"
        output_path = get_unique_filename(output_dir, output_name)

        if not self.is_ffmpeg_available():
            raise Exception(
                "FFmpeg is not installed. Please install it from https://ffmpeg.org/download.html"
            )

        cmd = [FFMPEG_PATH, "-y", "-i", input_path]

        # Video codec selection based on format
        if ext == "mp4":
            cmd.extend(["-c:v", "libx264"])
        elif ext == "webm":
            cmd.extend(["-c:v", "libvpx-vp9"])
        elif ext == "avi":
            cmd.extend(["-c:v", "mpeg4"])
        elif ext == "mov":
            cmd.extend(["-c:v", "libx264"])
        elif ext == "mkv":
            cmd.extend(["-c:v", "libx264"])

        # Resolution
        if resolution and resolution != "original":
            scale = self.RESOLUTION_MAP.get(resolution)
            if scale:
                cmd.extend(["-vf", f"scale={scale}"])

        # Bitrate
        if bitrate:
            cmd.extend(["-b:v", f"{bitrate}k"])

        # Preset
        ffmpeg_preset = self.PRESET_MAP.get(preset, "medium")
        cmd.extend(["-preset", ffmpeg_preset])

        # Audio copy
        cmd.extend(["-c:a", "copy"])

        # Output
        cmd.append(output_path)

        duration = self._get_duration(input_path)

        self._process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

        # Parse progress
        for line in self._process.stdout:
            if self._cancelled:
                self._process.terminate()
                raise Exception("Conversion cancelled.")

            if duration and self.progress_callback:
                time_match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)
                if time_match:
                    hours, minutes, seconds = map(float, time_match.groups())
                    current_time = hours * 3600 + minutes * 60 + seconds
                    percent = min((current_time / duration) * 100, 100)
                    self.progress_callback(input_path, "processing", percent)

        self._process.wait()
        if self._process.returncode != 0:
            raise Exception("FFmpeg conversion failed.")

        return output_path

    def convert_batch(
        self,
        file_paths,
        output_format,
        output_dir=None,
        resolution=None,
        bitrate=None,
        preset="medium",
    ):
        """Convert multiple videos sequentially in a background thread."""

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
                        resolution,
                        bitrate,
                        preset,
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
