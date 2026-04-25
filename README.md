# Universal Media Converter

A cross-platform desktop application for converting videos, images, and documents — built with Python and CustomTkinter.

## Features

- **Video Converter** — Convert between MP4, AVI, MOV, MKV, WEBM with resolution, bitrate, and compression controls
- **Image Converter** — Convert between JPG, PNG, WEBP, BMP, TIFF with resize and quality options
- **Document Converter** — Convert between PDF, DOCX, TXT, HTML with formatting preservation
- **Batch Processing** — Queue and convert multiple files at once
- **Drag & Drop** — Simple file selection with native dialogs and drag-and-drop support
- **Progress Tracking** — Real-time progress bars and status updates
- **Dark Modern UI** — Clean, professional interface built with CustomTkinter

## Requirements

- Python 3.10+
- FFmpeg (for video conversion)
- Pandoc (for document conversion)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/username/Universal-Media-Converter.git
   cd Universal-Media-Converter
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install FFmpeg:
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Add to your system PATH

4. Install Pandoc:
   - Download from [pandoc.org](https://pandoc.org/installing.html)
   - Add to your system PATH

## Running the App

```bash
python src/main.py
```

## Building the Executable

```bash
python build.py
```

The executable will be created in the `dist/` folder.

## Development Plan

See [plan.md](plan.md) for the full phased development roadmap.

## License

MIT
