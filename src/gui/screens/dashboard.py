"""Dashboard screen with converter category cards."""

import customtkinter as ctk
from config import APP_NAME, THEME
from gui.components.converter_card import ConverterCard


class DashboardScreen(ctk.CTkFrame):
    """Home screen displaying converter category cards."""

    def __init__(self, parent, navigate_callback, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.navigate_callback = navigate_callback

        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkLabel(
            self,
            text=APP_NAME,
            font=(THEME["font_family"], 32, "bold"),
            text_color=THEME["text"],
        )
        header.pack(pady=(40, 10))

        subtitle = ctk.CTkLabel(
            self,
            text="Convert Videos, Images & Documents — Fast & Easy",
            font=(THEME["font_family"], 14),
            text_color=THEME["text_secondary"],
        )
        subtitle.pack(pady=(0, 50))

        # Cards container
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(expand=True)

        # Video Converter Card
        video_card = ConverterCard(
            cards_frame,
            title="Video Converter",
            description="Convert between MP4, AVI, MOV, MKV, WEBM with resolution and bitrate controls.",
            icon_text="🎬",
            command=lambda: self.navigate_callback("video"),
        )
        video_card.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        # Image Converter Card
        image_card = ConverterCard(
            cards_frame,
            title="Image Converter",
            description="Convert between JPG, PNG, WEBP, BMP, TIFF with resize and quality options.",
            icon_text="🖼️",
            command=lambda: self.navigate_callback("image"),
        )
        image_card.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        # Document Converter Card
        doc_card = ConverterCard(
            cards_frame,
            title="Document Converter",
            description="Convert between PDF, DOCX, TXT, HTML with formatting preservation.",
            icon_text="📄",
            command=lambda: self.navigate_callback("document"),
        )
        doc_card.grid(row=0, column=2, padx=15, pady=15, sticky="nsew")

        # Footer
        footer = ctk.CTkLabel(
            self,
            text="Select a converter to get started",
            font=(THEME["font_family"], 12),
            text_color=THEME["text_secondary"],
        )
        footer.pack(pady=(50, 20))
