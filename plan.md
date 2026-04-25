# Universal Media Converter — Development Plan

> Derived from `universal_media_converter_sdd.md` (Spec-Driven Development Document v2.0)
> **Platform:** Desktop Application (Windows, cross-platform capable)

---

## Overview

This plan builds the **Universal Media Converter** as a **Python desktop application** using **CustomTkinter** for a modern, dark-themed native UI. The app runs locally on your machine — no web server, no browser, no cloud upload required.

**Architecture:**

- **GUI Framework:** Python + CustomTkinter (modern tkinter with dark mode, rounded widgets)
- **Concurrency:** Python `threading` for background conversions (keeps UI responsive)
- **Conversion Engines:**
  - **Video:** FFmpeg (via subprocess)
  - **Image:** Pillow (PIL)
  - **Document:** Pandoc (primary), python-docx / ReportLab (fallbacks)
- **Packaging:** PyInstaller (to build `.exe` distributable)
- **Storage:** Local filesystem only — user selects input files and output folder

**Repository:** `Universal-Media-Converter`
**Branching:** `main` — each phase committed and pushed to GitHub

---

## Phase 1: Project Setup & Core Structure

**Goal:** Initialize Python project, install dependencies, and create the app shell.

**Tasks:**

1. Create folder structure:
   ```
   universal-media-converter/
   ├── src/
   │   ├── main.py
   │   ├── gui/
   │   │   ├── app.py
   │   │   ├── components/
   │   │   └── themes/
   │   ├── converters/
   │   │   ├── image_converter.py
   │   │   ├── document_converter.py
   │   │   └── video_converter.py
   │   ├── utils/
   │   │   ├── file_utils.py
   │   │   └── validators.py
   │   └── config.py
   ├── assets/
   │   └── icons/
   ├── outputs/
   ├── tests/
   ├── requirements.txt
   ├── build.py (PyInstaller script)
   ├── .gitignore
   └── README.md
   ```
2. Create `requirements.txt` with:
   - `customtkinter`
   - `Pillow`
   - `pypandoc`
   - `python-docx`
   - `tkinterdnd2` (for drag-and-drop support)
   - `pyinstaller` (for building)
3. Set up `src/config.py` — app constants, supported formats, paths
4. Create `src/main.py` — entry point that launches the app
5. Create `src/gui/app.py` — main CustomTkinter window with:
   - App title and fixed responsive window size
   - Dark theme configuration (colors, fonts, rounded corners)
   - Basic frame/layout structure

**Deliverables:**

- App window opens with dark modern theme
- Folder structure is clean and organized
- All dependencies installable via `pip install -r requirements.txt`

**Git Checkpoint:** `chore: initialize desktop app project structure`

---

## Phase 2: Dashboard & Navigation

**Goal:** Build the home screen with converter category cards and screen navigation.

**Tasks:**

1. Create reusable GUI components in `src/gui/components/`:
   - `ConverterCard` — icon + title + description + CTA button (rounded card with shadow effect)
   - `Header` — app title/logo bar
   - `Footer` — status bar or version info
2. Build Dashboard screen:
   - Grid of 3 cards: Video Converter, Image Converter, Document Converter
   - Hover effects and animations (color shifts)
3. Implement screen navigation:
   - Dashboard → Video Converter screen
   - Dashboard → Image Converter screen
   - Dashboard → Document Converter screen
   - Back button on each converter screen to return to Dashboard
4. Create placeholder converter screens with "Coming Soon" text

**Deliverables:**

- Clicking a card navigates to the correct converter screen
- Back button returns to dashboard
- UI feels modern and responsive within window bounds

**Git Checkpoint:** `feat: dashboard with converter cards and navigation`

---

## Phase 3: File Selection & Queue Management

**Goal:** Build the file picker, drag-and-drop, and batch queue UI shared across all converters.

**Tasks:**

1. Create `src/gui/components/FileSelector.py`:
   - "Select Files" button opening native file dialog
   - Drag-and-drop zone using `tkinterdnd2`
   - Display selected files in a scrollable list
   - Per-file info: name, size, type, remove button
2. Create `src/gui/components/FileQueue.py`:
   - Scrollable frame showing queued files
   - Each row: filename, status badge, progress bar, remove button
   - Status states: Pending, Processing, Completed, Failed
3. Create `src/utils/file_utils.py`:
   - File size formatting
   - Filename sanitization
   - File type detection (extension + magic numbers via `python-magic` or manual check)
4. Create `src/utils/validators.py`:
   - Validate file types against converter support lists
   - Validate file size limits
   - Return user-friendly error messages
5. Wire file selection into placeholder converter screens

**Deliverables:**

- Users can select multiple files via dialog or drag-and-drop
- Invalid files show error toasts/notifications
- File queue displays correctly with all metadata

**Git Checkpoint:** `feat: file selection, drag-drop, and batch queue ui`

---

## Phase 4: Image Converter Module (End-to-End)

**Goal:** Complete vertical slice — select images, convert them, save output locally.

**Tasks:**

1. **GUI (`src/gui/screens/image_converter.py`):**
   - Format selector dropdown (JPG, PNG, WEBP, BMP, TIFF)
   - Advanced options panel (collapsible):
     - Resize: width × height inputs (optional, maintains aspect ratio by default)
     - Quality/compression slider (1–100)
     - Preserve transparency toggle (auto-disable for JPEG)
   - Output folder selector (default: `./outputs/`)
   - "Convert" button
   - Progress tracker using `FileQueue` component
   - "Open Output Folder" button after completion
2. **Backend (`src/converters/image_converter.py`):**
   - Use **Pillow** for all conversions
   - Support input: JPG, PNG, WEBP, BMP, TIFF, GIF
   - Support output: JPG, PNG, WEBP, BMP, TIFF
   - Implement resize with `LANCZOS` resampling
   - Implement quality/compression settings
   - Preserve alpha channel for formats that support it
   - Run in background thread, report progress
3. **Integration:**
   - Threading: conversion runs in `threading.Thread`, UI updates via `after()` or queue
   - Progress reporting: 0% → 100% based on files completed (or per-file if single)
   - Error handling: corrupted images, unsupported formats, disk full

**Deliverables:**

- Users can convert images with custom settings
- Output files saved to selected folder
- Batch image conversion works (multiple files processed sequentially)
- Progress visible in real-time, UI remains responsive

**Git Checkpoint:** `feat: image converter module with pillow backend`

---

## Phase 5: Document Converter Module (End-to-End)

**Goal:** Complete vertical slice — document format conversion using Pandoc and Python libraries.

**Tasks:**

1. **GUI (`src/gui/screens/document_converter.py`):**
   - Format selector dropdown (PDF, DOCX, TXT, HTML)
   - Advanced options:
     - Preserve formatting toggle (best-effort flag)
   - Output folder selector
   - "Convert" button + progress tracking
2. **Backend (`src/converters/document_converter.py`):**
   - Use **Pandoc** as primary engine (subprocess)
     - Support: MD → PDF/DOCX/TXT/HTML, HTML → PDF/DOCX/TXT, TXT → all
   - Use **python-docx** for DOCX-specific operations
   - Use **ReportLab** for simple TXT → PDF (fallback if Pandoc unavailable)
   - Validate conversion pairs (some may be unsupported — show error early)
3. **Integration:**
   - Background thread execution
   - Progress tracking
   - Handle Pandoc not installed — show helpful error message with install link

**Deliverables:**

- Document conversions are functional
- Pandoc auto-detected; graceful fallback if missing
- Unsupported format pairs show clear errors before conversion starts

**Git Checkpoint:** `feat: document converter module with pandoc backend`

---

## Phase 6: Video Converter Module (End-to-End)

**Goal:** Complete vertical slice — video conversion using FFmpeg.

**Tasks:**

1. **GUI (`src/gui/screens/video_converter.py`):**
   - Format selector dropdown (MP4, AVI, MOV, MKV, WEBM)
   - Advanced options panel:
     - Resolution dropdown (Original, 1080p, 720p, 480p, 360p)
     - Bitrate input (kbps, optional)
     - Compression preset (Fast, Medium, Slow — maps to FFmpeg presets)
   - Output folder selector
   - "Convert" button + progress tracking
2. **Backend (`src/converters/video_converter.py`):**
   - Use **FFmpeg** via subprocess
   - Support input: MP4, AVI, MOV, MKV, WMV, FLV, WEBM
   - Support output: MP4, AVI, MOV, MKV, WEBM
   - Implement resolution scaling (`-vf scale=`)
   - Implement bitrate control (`-b:v`)
   - Implement compression presets (`-preset`)
   - Parse FFmpeg stderr to extract real-time progress percentage
   - Run in background thread, stream progress back to UI
3. **Integration:**
   - FFmpeg auto-detection on startup
   - If FFmpeg missing, show error with installation instructions
   - Large file handling — process without loading into memory

**Deliverables:**

- Video conversions are functional
- Progress bar updates accurately during long conversions
- UI stays responsive even on large video files

**Git Checkpoint:** `feat: video converter module with ffmpeg backend`

---

## Phase 7: Batch Processing, Progress & Polish

**Goal:** Make batch workflows robust, add UI polish, and ensure performance targets.

**Tasks:**

1. **Batch Processing:**
   - All three converters support multi-file selection
   - Queue processes files sequentially (or configurable concurrent threads)
   - Per-file status tracking in `FileQueue`
   - "Stop All" and "Remove Completed" buttons
2. **Progress Tracking:**
   - Smooth progress bar animations
   - Estimated time remaining (based on file size and elapsed time)
   - Individual progress for each file in the queue
   - Toast/notification system for completion and errors
3. **UI/UX Polish:**
   - CustomTkinter theme refinements (consistent padding, rounded buttons, shadows)
   - Loading spinners during conversion
   - Empty states ("No files selected" illustration/message)
   - Error states with retry option
   - Success summaries ("5 files converted successfully")
4. **Security & Cleanup:**
   - Strict file validation (magic bytes + extension whitelist)
   - Temp file cleanup after conversion or on app exit
   - Sanitize all output filenames

**Deliverables:**

- Batch conversion is smooth and reliable
- UI feels polished and professional
- No temp files left behind
- Performance targets met (small files <5s, medium <30s)

**Git Checkpoint:** `feat: batch processing, progress tracking, and ui polish`

---

## Phase 8: Testing, Build & Distribution

**Goal:** Ensure the app is stable, tested, and packaged for desktop use.

**Tasks:**

1. **Testing:**
   - Unit tests for `validators.py` and `file_utils.py`
   - Unit tests for each converter module (with sample files)
   - GUI smoke tests (ensure screens open without errors)
2. **Build:**
   - Create `build.py` script using **PyInstaller**
   - Configure single `.exe` output with icon
   - Include assets, FFmpeg/Pandoc detection (bundle or instruct)
   - Test built `.exe` on a clean machine
3. **Documentation:**
   - Update `README.md` with:
     - Screenshots of the app
     - Installation instructions (Python + dependencies)
     - FFmpeg/Pandoc install guides
     - Build instructions
   - Add `CHANGELOG.md`
4. **Final QA against Acceptance Criteria:**
   - ✅ Users can select supported files
   - ✅ Users can select output formats
   - ✅ Files convert successfully
   - ✅ Progress is visible
   - ✅ Results are saved locally
   - ✅ Batch conversion works
   - ✅ Errors are handled gracefully

**Deliverables:**

- Test suite passes
- `dist/UniversalMediaConverter.exe` is generated
- Documentation is complete
- All acceptance criteria satisfied

**Git Checkpoint:** `docs: testing, build script, and final distribution`

---

## Git Workflow

**Commit Strategy:**

- Each phase is a **single commit** with a clear conventional commit message
- If a phase is very large, split into logical sub-commits within the phase, then push once complete

**Push Cadence:**

- At the end of **every phase**, run:
  ```bash
  git add .
  git commit -m "<phase message>"
  git push origin main
  ```

**Branching (Optional):**

- Create feature branches per phase if preferred:
  ```bash
  git checkout -b phase/<n>-<name>
  # ... work ...
  git push -u origin phase/<n>-<name>
  # merge via PR or git merge
  ```

---

## Tech Stack Summary

| Layer           | Technology                             |
| --------------- | -------------------------------------- |
| GUI Framework   | Python + CustomTkinter (+ tkinterdnd2) |
| Concurrency     | Python `threading`                     |
| Video Engine    | FFmpeg (subprocess)                    |
| Image Engine    | Pillow (PIL)                           |
| Document Engine | Pandoc, python-docx, ReportLab         |
| Utilities       | python-magic (file type detection)     |
| Packaging       | PyInstaller (single .exe)              |

---

## External Dependencies

| Tool   | Purpose             | Install Link / Command                 |
| ------ | ------------------- | -------------------------------------- |
| FFmpeg | Video conversion    | https://ffmpeg.org/download.html       |
| Pandoc | Document conversion | https://pandoc.org/installing.html     |
| Python | Runtime             | https://python.org (3.10+ recommended) |

> The app will detect missing tools on startup and prompt the user with install instructions.

---

## Risk Mitigation

| Risk                            | Mitigation                                                 |
| ------------------------------- | ---------------------------------------------------------- |
| FFmpeg/Pandoc not installed     | Auto-detect on startup; show friendly install instructions |
| UI freezes during conversion    | All conversions run in `threading.Thread`                  |
| Large video file processing     | Stream via FFmpeg (never load full video into memory)      |
| Unsupported format combinations | Validate before conversion; show clear error messages      |
| Corrupt input files             | Try/catch around conversion; mark as failed in queue       |
| Output filename conflicts       | Auto-append counter (e.g., `file (1).png`)                 |

---

## Estimates (Relative)

| Phase                       | Relative Effort |
| --------------------------- | --------------- |
| Phase 1: Setup              | Small           |
| Phase 2: Dashboard & Nav    | Small           |
| Phase 3: File Selection     | Medium          |
| Phase 4: Image Converter    | Medium          |
| Phase 5: Document Converter | Medium          |
| Phase 6: Video Converter    | Large           |
| Phase 7: Batch & Polish     | Medium          |
| Phase 8: Testing & Build    | Medium          |

**Total:** 8 phases, each pushed to GitHub upon completion.

---

## Next Step

Ready to begin **Phase 1: Project Setup & Core Structure**.

Toggle to **Act Mode** to start implementation.
