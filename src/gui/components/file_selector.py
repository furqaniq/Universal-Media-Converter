"""File selection component with native dialog and drag-and-drop."""

import customtkinter as ctk
from tkinter import filedialog
from config import THEME
from utils.file_utils import get_file_info


class FileSelector(ctk.CTkFrame):
    """Component for selecting files via dialog or drag-and-drop."""

    def __init__(self, parent, on_files_selected, filetypes=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.on_files_selected = on_files_selected
        self.filetypes = filetypes or [("All Files", "*.*")]

        self._build_ui()

    def _build_ui(self):
        # Drop zone frame
        self.drop_frame = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=THEME["border_radius"],
            border_width=2,
            border_color=THEME["accent"],
        )
        self.drop_frame.pack(fill="x", pady=10, ipady=30)

        # Icon
        icon = ctk.CTkLabel(
            self.drop_frame,
            text="📁",
            font=("Segoe UI Emoji", 36),
            text_color=THEME["highlight"],
        )
        icon.pack(pady=(20, 10))

        # Instruction text
        instruction = ctk.CTkLabel(
            self.drop_frame,
            text="Drag & drop files here or click to browse",
            font=(THEME["font_family"], 14),
            text_color=THEME["text_secondary"],
        )
        instruction.pack(pady=(5, 10))

        # Browse button
        browse_btn = ctk.CTkButton(
            self.drop_frame,
            text="Select Files",
            font=(THEME["font_family"], 12, "bold"),
            fg_color=THEME["accent"],
            hover_color=THEME["highlight"],
            corner_radius=THEME["border_radius"],
            command=self._browse_files,
        )
        browse_btn.pack(pady=(5, 20))

        # Bind drag-and-drop (basic highlight effect; full DnD in Phase 7)
        self.drop_frame.bind("<Enter>", self._on_drag_enter)
        self.drop_frame.bind("<Leave>", self._on_drag_leave)

    def _on_drag_enter(self, event=None):
        self.drop_frame.configure(border_color=THEME["highlight"])

    def _on_drag_leave(self, event=None):
        self.drop_frame.configure(border_color=THEME["accent"])

    def _browse_files(self):
        """Open native file dialog for multi-select."""
        files = filedialog.askopenfilenames(filetypes=self.filetypes)
        if files:
            file_infos = [get_file_info(f) for f in files]
            self.on_files_selected(file_infos)

    def get_supported_filetypes(self, converter_type):
        """Return filetypes tuple for a given converter."""
        from config import SUPPORTED_FORMATS
        exts = SUPPORTED_FORMATS.get(converter_type, {}).get("input", [])
        patterns = [(f"*.{ext}") for ext in exts]
        return [(f"{converter_type.title()} Files", " ".join(patterns))]
