"""File utility functions for formatting, sanitization, and type detection."""

import os
import re
from pathlib import Path


def format_file_size(size_bytes):
    """Format bytes into human-readable string."""
    if size_bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    index = 0
    while size_bytes >= 1024 and index < len(units) - 1:
        size_bytes /= 1024
        index += 1
    return f"{size_bytes:.1f} {units[index]}"


def sanitize_filename(filename):
    """Remove or replace invalid characters from filename."""
    name, ext = os.path.splitext(filename)
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = name.strip(". ")
    if not name:
        name = "file"
    return name + ext


def get_unique_filename(directory, filename):
    """Return a unique filename in the directory, appending a counter if needed."""
    directory = Path(directory)
    base = Path(sanitize_filename(filename))
    stem = base.stem
    suffix = base.suffix
    counter = 1
    result = directory / base
    while result.exists():
        result = directory / f"{stem} ({counter}){suffix}"
        counter += 1
    return str(result)


def get_file_extension(filepath):
    """Get lowercase file extension without dot."""
    return Path(filepath).suffix.lower().lstrip(".")


def detect_file_category(filepath):
    """Detect whether a file is video, image, or document based on extension."""
    ext = get_file_extension(filepath)
    video_exts = {"mp4", "avi", "mov", "mkv", "wmv", "flv", "webm"}
    image_exts = {"jpg", "jpeg", "png", "webp", "bmp", "tiff", "gif"}
    doc_exts = {"pdf", "docx", "txt", "html", "md"}
    if ext in video_exts:
        return "video"
    if ext in image_exts:
        return "image"
    if ext in doc_exts:
        return "document"
    return "unknown"


def get_file_info(filepath):
    """Return dict with file metadata."""
    path = Path(filepath)
    stat = path.stat()
    return {
        "path": str(path),
        "name": path.name,
        "size": stat.st_size,
        "size_formatted": format_file_size(stat.st_size),
        "extension": get_file_extension(filepath),
        "category": detect_file_category(filepath),
    }
