"""Validation utilities for files and conversion settings."""

import os
from config import SUPPORTED_FORMATS, MAX_FILE_SIZE


def validate_file(filepath, converter_type):
    """Validate a file for the given converter type.

    Returns (is_valid, error_message)
    """
    if not os.path.exists(filepath):
        return False, "File does not exist."

    if not os.path.isfile(filepath):
        return False, "Path is not a file."

    size = os.path.getsize(filepath)
    if size > MAX_FILE_SIZE:
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        return False, f"File exceeds maximum size of {max_mb:.0f} MB."

    ext = os.path.splitext(filepath)[1].lower().lstrip(".")
    allowed = SUPPORTED_FORMATS.get(converter_type, {}).get("input", [])
    if ext not in allowed:
        formats = ", ".join(allowed).upper()
        return False, f"Unsupported file type. Allowed: {formats}"

    return True, ""


def validate_output_format(output_format, converter_type):
    """Validate output format for the given converter type.

    Returns (is_valid, error_message)
    """
    allowed = SUPPORTED_FORMATS.get(converter_type, {}).get("output", [])
    if output_format.lower() not in allowed:
        formats = ", ".join(allowed).upper()
        return False, f"Unsupported output format. Allowed: {formats}"
    return True, ""


def validate_conversion_pair(input_path, output_format, converter_type):
    """Validate both input file and output format.

    Returns (is_valid, error_message)
    """
    valid, msg = validate_file(input_path, converter_type)
    if not valid:
        return False, msg

    valid, msg = validate_output_format(output_format, converter_type)
    if not valid:
        return False, msg

    return True, ""
