"""Document converter placeholder screen."""

import customtkinter as ctk
from config import THEME


class DocumentConverterScreen(ctk.CTkFrame):
    """Placeholder screen for document conversion."""

    def __init__(self, parent, back_callback, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.back_callback = back_callback
        self._build_ui()

    def _build_ui(self):
        # Header with back button
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(20, 30))

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
        back_btn.pack(side="left", padx=10)

        title = ctk.CTkLabel(
            header_frame,
            text="📄 Document Converter",
            font=(THEME["font_family"], 24, "bold"),
            text_color=THEME["text"],
        )
        title.pack(side="left", padx=20)

        # Placeholder content
        placeholder = ctk.CTkLabel(
            self,
            text="Document Converter — Coming in Phase 5",
            font=(THEME["font_family"], 16),
            text_color=THEME["text_secondary"],
        )
        placeholder.pack(expand=True)
