"""Main application window using CustomTkinter."""

import customtkinter as ctk
from config import APP_NAME, APP_WIDTH, APP_HEIGHT, THEME
from gui.screens.dashboard import DashboardScreen
from gui.screens.video_converter import VideoConverterScreen
from gui.screens.image_converter import ImageConverterScreen
from gui.screens.document_converter import DocumentConverterScreen


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

        # Main container frame for screen switching
        self.container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # Screens dictionary
        self.screens = {}
        self.current_screen = None

        self._create_screens()
        self.show_screen("dashboard")

    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - APP_WIDTH) // 2
        y = (screen_height - APP_HEIGHT) // 2
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")

    def _create_screens(self):
        """Initialize all application screens."""
        self.screens["dashboard"] = DashboardScreen(
            self.container,
            navigate_callback=self.show_screen,
        )

        self.screens["video"] = VideoConverterScreen(
            self.container,
            back_callback=lambda: self.show_screen("dashboard"),
        )

        self.screens["image"] = ImageConverterScreen(
            self.container,
            back_callback=lambda: self.show_screen("dashboard"),
        )

        self.screens["document"] = DocumentConverterScreen(
            self.container,
            back_callback=lambda: self.show_screen("dashboard"),
        )

    def show_screen(self, screen_name):
        """Switch to the specified screen."""
        if self.current_screen:
            self.current_screen.pack_forget()

        screen = self.screens.get(screen_name)
        if screen:
            screen.pack(fill="both", expand=True, padx=20, pady=20)
            self.current_screen = screen

    def run(self):
        """Start the main event loop."""
        self.root.mainloop()
