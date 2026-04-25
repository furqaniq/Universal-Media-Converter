"""File queue component showing selected files and conversion status."""

import customtkinter as ctk
from config import THEME


class FileQueue(ctk.CTkFrame):
    """Scrollable list of files with status badges and progress bars."""

    STATUS_COLORS = {
        "pending": THEME["text_secondary"],
        "processing": THEME["warning"],
        "completed": THEME["success"],
        "failed": THEME["error"],
    }

    def __init__(self, parent, on_remove=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.on_remove = on_remove
        self.rows = {}
        self._build_ui()

    def _build_ui(self):
        # Header with action buttons
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(10, 5))

        header = ctk.CTkLabel(
            header_frame,
            text="Selected Files",
            font=(THEME["font_family"], 16, "bold"),
            text_color=THEME["text"],
        )
        header.pack(side="left", padx=5)

        self.clear_btn = ctk.CTkButton(
            header_frame,
            text="Clear Completed",
            font=(THEME["font_family"], 10),
            fg_color=THEME["accent"],
            hover_color=THEME["highlight"],
            corner_radius=6,
            width=110,
            height=24,
            command=self.clear_completed,
        )
        self.clear_btn.pack(side="right", padx=5)

        self.stop_btn = ctk.CTkButton(
            header_frame,
            text="Stop All",
            font=(THEME["font_family"], 10),
            fg_color=THEME["error"],
            hover_color="#c0392b",
            corner_radius=6,
            width=70,
            height=24,
            command=self._on_stop_all,
        )
        self.stop_btn.pack(side="right", padx=5)

        # Scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=THEME["border_radius"],
            border_width=0,
        )
        self.scroll_frame.pack(fill="both", expand=True, pady=5)

        # Empty state label
        self.empty_label = ctk.CTkLabel(
            self.scroll_frame,
            text="No files selected",
            font=(THEME["font_family"], 12),
            text_color=THEME["text_secondary"],
        )
        self.empty_label.pack(pady=30)

    def _on_stop_all(self):
        """Emit stop signal to the parent handler."""
        if hasattr(self, "on_stop") and self.on_stop:
            self.on_stop()

    def add_files(self, file_infos):
        """Add multiple files to the queue."""
        self.empty_label.pack_forget()
        for info in file_infos:
            self._add_row(info)

    def _add_row(self, info):
        """Add a single file row."""
        path = info["path"]
        if path in self.rows:
            return

        row = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=5)

        # File info
        name_label = ctk.CTkLabel(
            row,
            text=info["name"],
            font=(THEME["font_family"], 12, "bold"),
            text_color=THEME["text"],
            anchor="w",
        )
        name_label.pack(side="left", padx=(5, 10))

        size_label = ctk.CTkLabel(
            row,
            text=info["size_formatted"],
            font=(THEME["font_family"], 11),
            text_color=THEME["text_secondary"],
        )
        size_label.pack(side="left", padx=5)

        # Status badge
        status_label = ctk.CTkLabel(
            row,
            text="Pending",
            font=(THEME["font_family"], 10, "bold"),
            text_color=THEME["bg"],
            fg_color=self.STATUS_COLORS["pending"],
            corner_radius=6,
            padx=8,
            pady=2,
        )
        status_label.pack(side="left", padx=10)

        # Progress bar (hidden initially)
        progress = ctk.CTkProgressBar(
            row,
            width=100,
            height=8,
            corner_radius=4,
            fg_color=THEME["accent"],
            progress_color=THEME["highlight"],
        )
        progress.set(0)

        # Remove button
        remove_btn = ctk.CTkButton(
            row,
            text="✕",
            font=(THEME["font_family"], 10, "bold"),
            fg_color="transparent",
            hover_color=THEME["error"],
            text_color=THEME["text_secondary"],
            width=28,
            height=28,
            corner_radius=6,
            command=lambda: self._remove_row(path),
        )
        remove_btn.pack(side="right", padx=5)

        self.rows[path] = {
            "frame": row,
            "status_label": status_label,
            "progress_bar": progress,
            "info": info,
        }

    def _remove_row(self, path):
        """Remove a file row from the queue."""
        if path in self.rows:
            self.rows[path]["frame"].destroy()
            del self.rows[path]
            if self.on_remove:
                self.on_remove(path)
            if not self.rows:
                self.empty_label.pack(pady=30)

    def update_status(self, path, status, progress=None):
        """Update status and progress for a file."""
        if path not in self.rows:
            return
        row = self.rows[path]
        color = self.STATUS_COLORS.get(status, THEME["text_secondary"])
        row["status_label"].configure(
            text=status.capitalize(),
            fg_color=color,
        )
        if status == "processing" and progress is not None:
            row["progress_bar"].pack(side="left", padx=5)
            row["progress_bar"].set(progress / 100)
        elif status in ("completed", "failed"):
            row["progress_bar"].pack_forget()

    def clear_completed(self):
        """Remove all completed files from the queue."""
        completed = [
            path for path, row in self.rows.items()
            if row["status_label"].cget("text").lower() == "completed"
        ]
        for path in completed:
            self._remove_row(path)

    def get_files(self):
        """Return list of file paths in the queue."""
        return [path for path in self.rows.keys()]

    def clear(self):
        """Remove all files from the queue."""
        for path in list(self.rows.keys()):
            self._remove_row(path)
