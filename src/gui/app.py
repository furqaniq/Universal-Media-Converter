"""Main application window using CustomTkinter."""

import customtkinter as ctk
from config import APP_NAME, APP_WIDTH, APP_HEIGHT, THEME


class App:
    """Main application class."""

    def __init__(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.root = ctk.CTk()
        self.root.title(APP_NAME)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.minsize(900, 600)
        self.root.configure(fg_color=THEME["bg"])

        # Center window on screen
        self._center_window()

        # Main container
        self.container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # Placeholder content for Phase 1
        self._build_placeholder()

    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - APP_WIDTH) // 2
        y = (screen_height - APP_HEIGHT) // 2
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")

    def _build_placeholder(self):
        """Build placeholder UI for Phase 1."""
        label = ctk.CTkLabel(
            self.container,
            text=APP_NAME,
            font=(THEME["font_family"], THEME["header_font_size"], "bold"),
            text_color=THEME["text"],
        )
        label.pack(pady=(100, 20))

        subtitle = ctk.CTkLabel(
            self.container,
            text="Desktop Media Converter — Phase 1 Initialized",
            font=(THEME["font_family"], THEME["font_size"]),
            text_color=THEME["text_secondary"],
        )
        subtitle.pack(pady=10)

        version_label = ctk.CTkLabel(
            self.container,
            text="Version 2.0 | Built with CustomTkinter",
            font=(THEME["font_family"], 12),
            text_color=THEME["text_secondary"],
        )
        version_label.pack(pady=10)

    def run(self):
        """Start the main event loop."""
        self.root.mainloop()
