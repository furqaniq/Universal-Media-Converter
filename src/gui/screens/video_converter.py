"""Video converter screen with options and backend integration."""

import customtkinter as ctk
from tkinter import filedialog
from config import THEME, VIDEO_OUTPUT_FORMATS, OUTPUTS_DIR
from gui.components.file_selector import FileSelector
from gui.components.file_queue import FileQueue
from utils.validators import validate_file
from converters.video_converter import VideoConverter


class VideoConverterScreen(ctk.CTkFrame):
    """Video converter screen with file selection, options, and queue."""

    def __init__(self, parent, back_callback, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.back_callback = back_callback
        self.queue = None
        self.converter = None
        self.output_dir = str(OUTPUTS_DIR)
        self._build_ui()

    def _build_ui(self):
        # Header with back button
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(10, 15))

        back_btn = ctk.CTkButton(
            header_frame,
            text="← Back",
            font=(THEME["font_family"], 12, "bold"),
            fg_color=THEME["accent"],
            hover_color=THEME["highlight"],
            corner_radius=THEME["border_radius"],
            width=80,
            command=self.back_callback,
        )
        back_btn.pack(side="left", padx=5)

        title = ctk.CTkLabel(
            header_frame,
            text="🎬 Video Converter",
            font=(THEME["font_family"], 22, "bold"),
            text_color=THEME["text"],
        )
        title.pack(side="left", padx=15)

        # Content area - two columns
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

        # Left: File selector
        filetypes = [("Video Files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm")]
        self.selector = FileSelector(
            content,
            on_files_selected=self._on_files_selected,
            filetypes=filetypes,
        )
        self.selector.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Right: File queue
        self.queue = FileQueue(content, on_remove=self._on_remove)
        self.queue.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Bottom: Options panel
        options_frame = ctk.CTkFrame(self, fg_color=THEME["card_bg"], corner_radius=THEME["border_radius"])
        options_frame.pack(fill="x", pady=10)

        # Output format
        format_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        format_frame.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            format_frame,
            text="Output Format:",
            font=(THEME["font_family"], 12, "bold"),
            text_color=THEME["text"],
        ).pack(side="left", padx=5)

        self.format_var = ctk.StringVar(value="mp4")
        self.format_menu = ctk.CTkOptionMenu(
            format_frame,
            values=[f.upper() for f in VIDEO_OUTPUT_FORMATS],
            variable=self.format_var,
            font=(THEME["font_family"], 12),
            dropdown_font=(THEME["font_family"], 12),
            fg_color=THEME["accent"],
            button_color=THEME["highlight"],
            corner_radius=THEME["border_radius"],
            width=120,
        )
        self.format_menu.pack(side="left", padx=10)

        # FFmpeg status
        self.ffmpeg_status = ctk.CTkLabel(
            format_frame,
            text="",
            font=(THEME["font_family"], 11),
        )
        self.ffmpeg_status.pack(side="left", padx=15)
        self._check_ffmpeg()

        # Resolution dropdown
        res_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        res_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            res_frame,
            text="Resolution:",
            font=(THEME["font_family"], 12, "bold"),
            text_color=THEME["text"],
        ).pack(side="left", padx=5)

        self.resolution_var = ctk.StringVar(value="original")
        self.resolution_menu = ctk.CTkOptionMenu(
            res_frame,
            values=["Original", "1080p", "720p", "480p", "360p"],
            variable=self.resolution_var,
            font=(THEME["font_family"], 12),
            dropdown_font=(THEME["font_family"], 12),
            fg_color=THEME["accent"],
            button_color=THEME["highlight"],
            corner_radius=THEME["border_radius"],
            width=120,
        )
        self.resolution_menu.pack(side="left", padx=10)

        # Bitrate input
        bitrate_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        bitrate_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            bitrate_frame,
            text="Bitrate (kbps, optional):",
            font=(THEME["font_family"], 12, "bold"),
            text_color=THEME["text"],
        ).pack(side="left", padx=5)

        self.bitrate_var = ctk.StringVar(value="")
        ctk.CTkEntry(
            bitrate_frame,
            textvariable=self.bitrate_var,
            font=(THEME["font_family"], 11),
            width=80,
            corner_radius=6,
        ).pack(side="left", padx=10)

        # Preset dropdown
        preset_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        preset_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            preset_frame,
            text="Compression Preset:",
            font=(THEME["font_family"], 12, "bold"),
            text_color=THEME["text"],
        ).pack(side="left", padx=5)

        self.preset_var = ctk.StringVar(value="medium")
        self.preset_menu = ctk.CTkOptionMenu(
            preset_frame,
            values=["Fast", "Medium", "Slow"],
            variable=self.preset_var,
            font=(THEME["font_family"], 12),
            dropdown_font=(THEME["font_family"], 12),
            fg_color=THEME["accent"],
            button_color=THEME["highlight"],
            corner_radius=THEME["border_radius"],
            width=120,
        )
        self.preset_menu.pack(side="left", padx=10)

        # Output folder selector
        folder_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        folder_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            folder_frame,
            text="Output Folder:",
            font=(THEME["font_family"], 12, "bold"),
            text_color=THEME["text"],
        ).pack(side="left", padx=5)

        self.folder_label = ctk.CTkLabel(
            folder_frame,
            text=self.output_dir,
            font=(THEME["font_family"], 11),
            text_color=THEME["text_secondary"],
        )
        self.folder_label.pack(side="left", padx=10)

        ctk.CTkButton(
            folder_frame,
            text="Change",
            font=(THEME["font_family"], 11),
            fg_color=THEME["accent"],
            hover_color=THEME["highlight"],
            corner_radius=THEME["border_radius"],
            width=80,
            command=self._select_output_folder,
        ).pack(side="left", padx=5)

        # Convert button
        btn_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(10, 15))

        self.convert_btn = ctk.CTkButton(
            btn_frame,
            text="Convert",
            font=(THEME["font_family"], 14, "bold"),
            fg_color=THEME["highlight"],
            hover_color="#d63a55",
            corner_radius=THEME["border_radius"],
            height=40,
            command=self._start_conversion,
        )
        self.convert_btn.pack(side="left", padx=5)

        self.open_folder_btn = ctk.CTkButton(
            btn_frame,
            text="Open Output Folder",
            font=(THEME["font_family"], 12),
            fg_color=THEME["accent"],
            hover_color=THEME["highlight"],
            corner_radius=THEME["border_radius"],
            command=self._open_output_folder,
        )
        self.open_folder_btn.pack(side="left", padx=10)

    def _check_ffmpeg(self):
        """Check FFmpeg availability and update UI."""
        if VideoConverter.is_ffmpeg_available():
            self.ffmpeg_status.configure(text="✓ FFmpeg detected", text_color=THEME["success"])
        else:
            self.ffmpeg_status.configure(
                text="✗ FFmpeg not found — install from ffmpeg.org",
                text_color=THEME["error"],
            )

    def _select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir = folder
            self.folder_label.configure(text=folder)

    def _open_output_folder(self):
        import os
        os.startfile(self.output_dir)

    def _on_files_selected(self, file_infos):
        valid = []
        for info in file_infos:
            ok, msg = validate_file(info["path"], "video")
            if ok:
                valid.append(info)
            else:
                print(f"Skipped {info['name']}: {msg}")
        if valid:
            self.queue.add_files(valid)

    def _on_remove(self, path):
        pass

    def _start_conversion(self):
        files = self.queue.get_files()
        if not files:
            return

        if not VideoConverter.is_ffmpeg_available():
            print("FFmpeg is not installed!")
            return

        self.convert_btn.configure(state="disabled", text="Converting...")
        output_format = self.format_var.get().lower()
        resolution = self.resolution_var.get().lower()
        bitrate = int(self.bitrate_var.get()) if self.bitrate_var.get().isdigit() else None
        preset = self.preset_var.get().lower()

        self.converter = VideoConverter(
            progress_callback=self._on_progress,
            completion_callback=self._on_complete,
        )
        self.converter.convert_batch(
            file_paths=files,
            output_format=output_format,
            output_dir=self.output_dir,
            resolution=resolution,
            bitrate=bitrate,
            preset=preset,
        )

    def _on_progress(self, path, status, progress):
        self.after(0, lambda: self.queue.update_status(path, status, progress))

    def _on_complete(self, results):
        self.after(0, self._reset_ui)
        success = sum(1 for _, ok, _ in results if ok)
        total = len(results)
        print(f"Converted {success}/{total} videos")

    def _reset_ui(self):
        self.convert_btn.configure(state="normal", text="Convert")
