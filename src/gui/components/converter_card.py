"""Reusable converter category card component."""

import customtkinter as ctk
from config import THEME


class ConverterCard(ctk.CTkFrame):
    """A clickable card representing a converter category."""

    def __init__(self, parent, title, description, icon_text, command, **kwargs):
        super().__init__(
            parent,
            fg_color=THEME["card_bg"],
            corner_radius=THEME["border_radius"],
            border_width=0,
            **kwargs,
        )

        self.command = command
        self._hover = False

        # Icon
        self.icon_label = ctk.CTkLabel(
            self,
            text=icon_text,
            font=("Segoe UI Emoji", 48),
            text_color=THEME["highlight"],
        )
        self.icon_label.pack(pady=(30, 10))

        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=(THEME["font_family"], THEME["card_font_size"], "bold"),
            text_color=THEME["text"],
        )
        self.title_label.pack(pady=(10, 5))

        # Description
        self.desc_label = ctk.CTkLabel(
            self,
            text=description,
            font=(THEME["font_family"], 12),
            text_color=THEME["text_secondary"],
            wraplength=220,
            justify="center",
        )
        self.desc_label.pack(pady=(0, 20))

        # CTA Button
        self.button = ctk.CTkButton(
            self,
            text="Start Conversion",
            font=(THEME["font_family"], 12, "bold"),
            fg_color=THEME["accent"],
            hover_color=THEME["highlight"],
            corner_radius=THEME["border_radius"],
            command=self._on_click,
        )
        self.button.pack(pady=(0, 30))

        # Bind hover effects to the entire card
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        for child in self.winfo_children():
            child.bind("<Enter>", self._on_enter)
            child.bind("<Leave>", self._on_leave)

    def _on_enter(self, event=None):
        if not self._hover:
            self._hover = True
            self.configure(border_width=2, border_color=THEME["highlight"])

    def _on_leave(self, event=None):
        self._hover = False
        self.configure(border_width=0)

    def _on_click(self):
        if self.command:
            self.command()
