"""Application configuration and constants."""

import os
from pathlib import Path

# Application info
APP_NAME = "Universal Media Converter"
APP_VERSION = "2.0"
APP_WIDTH = 1100
APP_HEIGHT = 700

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
ASSETS_DIR = BASE_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"

# Ensure outputs directory exists
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# Supported formats
VIDEO_INPUT_FORMATS = ["mp4", "avi", "mov", "mkv", "wmv", "flv", "webm"]
VIDEO_OUTPUT_FORMATS = ["mp4", "avi", "mov", "mkv", "webm"]

IMAGE_INPUT_FORMATS = ["jpg", "jpeg", "png", "webp", "bmp", "tiff", "gif"]
IMAGE_OUTPUT_FORMATS = ["jpg", "jpeg", "png", "webp", "bmp", "tiff"]

DOCUMENT_INPUT_FORMATS = ["pdf", "docx", "txt", "html", "md"]
DOCUMENT_OUTPUT_FORMATS = ["pdf", "docx", "txt", "html"]

# Format categories
SUPPORTED_FORMATS = {
    "video": {
        "input": VIDEO_INPUT_FORMATS,
        "output": VIDEO_OUTPUT_FORMATS,
    },
    "image": {
        "input": IMAGE_INPUT_FORMATS,
        "output": IMAGE_OUTPUT_FORMATS,
    },
    "document": {
        "input": DOCUMENT_INPUT_FORMATS,
        "output": DOCUMENT_OUTPUT_FORMATS,
    },
}

# File size limits (in bytes)
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2 GB

# UI theme
THEME = {
    "bg": "#1a1a2e",
    "card_bg": "#16213e",
    "accent": "#0f3460",
    "highlight": "#e94560",
    "text": "#eeeeee",
    "text_secondary": "#a0a0a0",
    "success": "#4ecca3",
    "warning": "#f4d03f",
    "error": "#e74c3c",
    "border_radius": 12,
    "font_family": "Segoe UI",
    "font_size": 14,
    "header_font_size": 24,
    "card_font_size": 16,
}

# External tool paths (can be overridden via env vars)
FFMPEG_PATH = os.environ.get("FFMPEG_PATH", "ffmpeg")
PANDOC_PATH = os.environ.get("PANDOC_PATH", "pandoc")
