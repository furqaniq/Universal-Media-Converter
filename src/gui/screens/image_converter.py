"""Image converter screen with file selection and queue."""

import customtkinter as ctk
from config import THEME
from gui.components.file_selector import FileSelector
from gui.components.file_queue import FileQueue
from utils.validators import validate_file


class ImageConverterScreen(ctk.CTkFrame):
    """Image converter screen with file selection, options, and queue."""

    def __init__(self, parent, back_callback, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.back_callback = back_callback
        self.queue = None
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
            text="🖼️ Image Converter",
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
        filetypes = [("Image Files", "*.jpg *.jpeg *.png *.webp *.bmp *.tiff *.gif")]
        self.selector = FileSelector(
            content,
            on_files_selected=self._on_files_selected,
            filetypes=filetypes,
        )
        self.selector.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Right: File queue
        self.queue = FileQueue(content, on_remove=self._on_remove)
        self.queue.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Bottom: Options placeholder
        options_frame = ctk.CTkFrame(self, fg_color=THEME["card_bg"], corner_radius=THEME["border_radius"])
        options_frame.pack(fill="x", pady=10)

        options_label = ctk.CTkLabel(
            options_frame,
            text="Output Format & Options — Coming in Phase 4",
            font=(THEME["font_family"], 12),
            text_color=THEME["text_secondary"],
        )
        options_label.pack(pady=15)

    def _on_files_selected(self, file_infos):
        """Handle files dropped or selected."""
        valid = []
        for info in file_infos:
            ok, msg = validate_file(info["path"], "image")
            if ok:
                valid.append(info)
            else:
                print(f"Skipped {info['name']}: {msg}")
        if valid:
            self.queue.add_files(valid)

    def _on_remove(self, path):
        """Handle file removal from queue."""
        pass
