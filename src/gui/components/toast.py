"""Toast notification component for success/error messages."""

import customtkinter as ctk
from config import THEME


class Toast(ctk.CTkFrame):
    """A temporary notification toast that auto-dismisses."""

    def __init__(self, parent, message, message_type="info", duration=3000, **kwargs):
        super().__init__(parent, **kwargs)
        self.duration = duration

        colors = {
            "info": (THEME["accent"], THEME["text"]),
            "success": (THEME["success"], THEME["bg"]),
            "warning": (THEME["warning"], THEME["bg"]),
            "error": (THEME["error"], THEME["text"]),
        }
        bg, fg = colors.get(message_type, colors["info"])

        self.configure(fg_color=bg, corner_radius=THEME["border_radius"])

        self.label = ctk.CTkLabel(
            self,
            text=message,
            font=(THEME["font_family"], 12, "bold"),
            text_color=fg,
            padx=15,
            pady=10,
        )
        self.label.pack()

        self.after(duration, self.destroy)


class ToastManager:
    """Manages toast notifications anchored to a parent widget."""

    def __init__(self, parent):
        self.parent = parent
        self.toasts = []

    def show(self, message, message_type="info", duration=3000):
        """Display a new toast notification."""
        toast = Toast(self.parent, message, message_type, duration)
        toast.place(relx=0.5, rely=0.9, anchor="center")
        self.toasts.append(toast)

        # Clean up old toasts
        self.toasts = [t for t in self.toasts if t.winfo_exists()]
