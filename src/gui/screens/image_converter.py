"""Image converter screen with full options and backend integration."""

import customtkinter as ctk
from tkinter import filedialog
from config import THEME, IMAGE_OUTPUT_FORMATS, OUTPUTS_DIR
from gui.components.file_selector import FileSelector
from gui.components.file_queue import FileQueue
from gui.components.toast import ToastManager
from utils.validators import validate_file
from converters.image_converter import ImageConverter


class ImageConverterScreen(ctk.CTkFrame):
    """Image converter screen with file selection, options, and queue."""

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

        self.format_var = ctk.StringVar(value="png")
        self.format_menu = ctk.CTkOptionMenu(
            format_frame,
            values=[f.upper() for f in IMAGE_OUTPUT_FORMATS],
            variable=self.format_var,
            font=(THEME["font_family"], 12),
            dropdown_font=(THEME["font_family"], 12),
            fg_color=THEME["accent"],
            button_color=THEME["highlight"],
            corner_radius=THEME["border_radius"],
            width=120,
        )
        self.format_menu.pack(side="left", padx=10)

        # Resize options
        resize_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        resize_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            resize_frame,
            text="Resize (optional):",
            font=(THEME["font_family"], 12, "bold"),
            text_color=THEME["text"],
        ).pack(side="left", padx=5)

        self.width_var = ctk.StringVar(value="")
        self.height_var = ctk.StringVar(value="")

        ctk.CTkLabel(resize_frame, text="W:", font=(THEME["font_family"], 11), text_color=THEME["text_secondary"]).pack(side="left", padx=(10, 2))
        ctk.CTkEntry(
            resize_frame,
            textvariable=self.width_var,
            font=(THEME["font_family"], 11),
            width=60,
            corner_radius=6,
        ).pack(side="left", padx=2)

        ctk.CTkLabel(resize_frame, text="H:", font=(THEME["font_family"], 11), text_color=THEME["text_secondary"]).pack(side="left", padx=(10, 2))
        ctk.CTkEntry(
            resize_frame,
            textvariable=self.height_var,
            font=(THEME["font_family"], 11),
            width=60,
            corner_radius=6,
        ).pack(side="left", padx=2)

        # Quality slider
        quality_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        quality_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            quality_frame,
            text="Quality:",
            font=(THEME["font_family"], 12, "bold"),
            text_color=THEME["text"],
        ).pack(side="left", padx=5)

        self.quality_var = ctk.IntVar(value=95)
        self.quality_slider = ctk.CTkSlider(
            quality_frame,
            from_=1,
            to=100,
            number_of_steps=99,
            variable=self.quality_var,
            width=200,
            progress_color=THEME["highlight"],
            button_color=THEME["highlight"],
        )
        self.quality_slider.pack(side="left", padx=10)

        self.quality_label = ctk.CTkLabel(
            quality_frame,
            text="95",
            font=(THEME["font_family"], 11),
            text_color=THEME["text_secondary"],
            width=30,
        )
        self.quality_label.pack(side="left", padx=5)
        self.quality_slider.configure(command=self._update_quality_label)

        # Preserve transparency
        self.transparency_var = ctk.BooleanVar(value=True)
        self.transparency_check = ctk.CTkCheckBox(
            options_frame,
            text="Preserve transparency when possible",
            variable=self.transparency_var,
            font=(THEME["font_family"], 11),
            text_color=THEME["text_secondary"],
            fg_color=THEME["accent"],
            hover_color=THEME["highlight"],
            corner_radius=6,
        )
        self.transparency_check.pack(anchor="w", padx=15, pady=5)

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

    def _update_quality_label(self, value):
        self.quality_label.configure(text=f"{int(value)}")

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
            ok, msg = validate_file(info["path"], "image")
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

        self.convert_btn.configure(state="disabled", text="Converting...")

        width = int(self.width_var.get()) if self.width_var.get().isdigit() else None
        height = int(self.height_var.get()) if self.height_var.get().isdigit() else None
        quality = self.quality_var.get()
        preserve = self.transparency_var.get()
        output_format = self.format_var.get().lower()

        self.converter = ImageConverter(
            progress_callback=self._on_progress,
            completion_callback=self._on_complete,
        )
        self.converter.convert_batch(
            file_paths=files,
            output_format=output_format,
            output_dir=self.output_dir,
            width=width,
            height=height,
            quality=quality,
            preserve_transparency=preserve,
        )

    def _on_progress(self, path, status, progress):
        self.after(0, lambda: self.queue.update_status(path, status, progress))

    def _on_complete(self, results):
        self.after(0, self._reset_ui)
        success = sum(1 for _, ok, _ in results if ok)
        total = len(results)
        if success == total:
            self.toast.show(f"All {total} images converted successfully!", "success")
        elif success > 0:
            self.toast.show(f"Converted {success}/{total} images. Check queue for errors.", "warning")
        else:
            self.toast.show("All conversions failed. Check console for details.", "error")

    def _reset_ui(self):
        self.convert_btn.configure(state="normal", text="Convert")
