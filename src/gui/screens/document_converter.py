"""Document converter screen with options and backend integration."""

import customtkinter as ctk
from tkinter import filedialog
from config import THEME, DOCUMENT_OUTPUT_FORMATS, OUTPUTS_DIR
from gui.components.file_selector import FileSelector
from gui.components.file_queue import FileQueue
from gui.components.toast import ToastManager
from utils.validators import validate_file
from converters.document_converter import DocumentConverter


class DocumentConverterScreen(ctk.CTkFrame):
    """Document converter screen with file selection, options, and queue."""

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
            text="📄 Document Converter",
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
        filetypes = [("Document Files", "*.pdf *.docx *.txt *.html *.md")]
        self.selector = FileSelector(
            content,
            on_files_selected=self._on_files_selected,
            filetypes=filetypes,
        )
        self.selector.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Right: File queue
        self.queue = FileQueue(content, on_remove=self._on_remove, on_stop=self._on_stop)
        self.queue.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.toast = ToastManager(self)

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

        self.format_var = ctk.StringVar(value="pdf")
        self.format_menu = ctk.CTkOptionMenu(
            format_frame,
            values=[f.upper() for f in DOCUMENT_OUTPUT_FORMATS],
            variable=self.format_var,
            font=(THEME["font_family"], 12),
            dropdown_font=(THEME["font_family"], 12),
            fg_color=THEME["accent"],
            button_color=THEME["highlight"],
            corner_radius=THEME["border_radius"],
            width=120,
        )
        self.format_menu.pack(side="left", padx=10)

        # Pandoc status
        self.pandoc_status = ctk.CTkLabel(
            format_frame,
            text="",
            font=(THEME["font_family"], 11),
        )
        self.pandoc_status.pack(side="left", padx=15)
        self._check_pandoc()

        # Preserve formatting
        self.formatting_var = ctk.BooleanVar(value=True)
        self.formatting_check = ctk.CTkCheckBox(
            options_frame,
            text="Preserve formatting (best effort)",
            variable=self.formatting_var,
            font=(THEME["font_family"], 11),
            text_color=THEME["text_secondary"],
            fg_color=THEME["accent"],
            hover_color=THEME["highlight"],
            corner_radius=6,
        )
        self.formatting_check.pack(anchor="w", padx=15, pady=5)

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

    def _check_pandoc(self):
        """Check Pandoc availability and update UI."""
        if DocumentConverter.is_pandoc_available():
            self.pandoc_status.configure(text="✓ Pandoc detected", text_color=THEME["success"])
        else:
            self.pandoc_status.configure(
                text="✗ Pandoc not found — install from pandoc.org",
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
            ok, msg = validate_file(info["path"], "document")
            if ok:
                valid.append(info)
            else:
                print(f"Skipped {info['name']}: {msg}")
        if valid:
            self.queue.add_files(valid)

    def _on_remove(self, path):
        pass

    def _on_stop(self):
        if self.converter:
            self.converter.cancel()
            self.toast.show("Conversion stopped", "warning")
        self._reset_ui()

    def _start_conversion(self):
        files = self.queue.get_files()
        if not files:
            return

        if not DocumentConverter.is_pandoc_available():
            print("Pandoc is not installed!")
            return

        self.convert_btn.configure(state="disabled", text="Converting...")
        output_format = self.format_var.get().lower()

        self.converter = DocumentConverter(
            progress_callback=self._on_progress,
            completion_callback=self._on_complete,
        )
        self.converter.convert_batch(
            file_paths=files,
            output_format=output_format,
            output_dir=self.output_dir,
        )

    def _on_progress(self, path, status, progress):
        self.after(0, lambda: self.queue.update_status(path, status, progress))

    def _on_complete(self, results):
        self.after(0, self._reset_ui)
        success = sum(1 for _, ok, _ in results if ok)
        total = len(results)
        if success == total:
            self.toast.show(f"All {total} documents converted successfully!", "success")
        elif success > 0:
            self.toast.show(f"Converted {success}/{total} documents. Check queue for errors.", "warning")
        else:
            self.toast.show("All conversions failed. Check console for details.", "error")

    def _reset_ui(self):
        self.convert_btn.configure(state="normal", text="Convert")
