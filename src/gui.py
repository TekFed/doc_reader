# gui.py
"""Main GUI implementation using Tkinter."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from pathlib import Path

from constants import *
from text_extraction import extract_text
from speech_engine import (
    get_available_voices,
    prefer_stable_voice,
    save_text_to_mp3,
    create_auto_mp3_filename,
)


class DocumentReaderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)  # noqa: F405
        self.root.configure(bg=WINDOW_BG)  # noqa: F405
        self.root.resizable(True, True)

        # Scrollable canvas setup
        self.canvas = tk.Canvas(self.root, bg=WINDOW_BG, highlightthickness=0)  # noqa: F405
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Mouse wheel support
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # State variables
        self.file_path: Path | None = None
        self.full_text = ""
        self.voices = []
        self.current_voice_id = None
        self.speaking_thread = None

        self.build_gui()
        self.load_voices()

    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self.window_id, width=event.width)

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")

    def build_gui(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Header
        header = tk.Frame(self.scrollable_frame, bg=HEADER_BG, height=60)  # noqa: F405
        header.pack(fill="x", pady=(0, 10))
        tk.Label(
            header, text=APP_TITLE,  # noqa: F405
            font=(FONT_FAMILY, 18, "bold"), fg=HEADER_FG, bg=HEADER_BG  # noqa: F405
        ).pack(pady=10)

        # File selection
        file_frame = ttk.LabelFrame(self.scrollable_frame, text="📄 Select Document", padding=10)
        file_frame.pack(fill="x", padx=15, pady=5)

        self.file_entry = ttk.Entry(file_frame, width=80, font=(FONT_FAMILY, 10))  # noqa: F405
        self.file_entry.pack(side="left", padx=5, fill="x", expand=True)

        ttk.Button(file_frame, text="Browse", command=self.browse_file).pack(side="right", padx=5)
        ttk.Button(file_frame, text="Load & Preview", command=self.load_file).pack(side="right", padx=5)

        # Preview
        preview_frame = ttk.LabelFrame(self.scrollable_frame, text="📝 Preview", padding=10)
        preview_frame.pack(fill="both", expand=True, padx=15, pady=5)
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame, height=PREVIEW_HEIGHT, wrap=tk.WORD, font=("Consolas", 10)  # noqa: F405
        )
        self.preview_text.pack(fill="both", expand=True)

        # Settings
        control_frame = ttk.LabelFrame(self.scrollable_frame, text="⚙️ Settings", padding=15)
        control_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(control_frame, text="Voice:").grid(row=0, column=0, sticky="w", pady=5)
        self.voice_combo = ttk.Combobox(control_frame, state="readonly", width=45)
        self.voice_combo.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        tk.Label(control_frame, text="Speed (wpm):").grid(row=1, column=0, sticky="w", pady=5)
        self.speed_var = tk.IntVar(value=DEFAULT_RATE)  # noqa: F405
        self.speed_slider = ttk.Scale(
            control_frame, from_=RATE_MIN, to=RATE_MAX,  # noqa: F405
            variable=self.speed_var, orient="horizontal", length=320
        )
        self.speed_slider.grid(row=1, column=1, sticky="w", padx=10)
        self.speed_label = tk.Label(control_frame, text=str(DEFAULT_RATE), font=(FONT_FAMILY, 10, "bold"))  # noqa: F405
        self.speed_label.grid(row=1, column=2, padx=5)
        self.speed_slider.configure(command=lambda v: self.speed_label.config(text=str(int(float(v)))))

        tk.Label(control_frame, text="Mode:").grid(row=2, column=0, sticky="w", pady=8)
        self.mode_var = tk.StringVar(value="save")

        # Live speak – disabled / coming soon
        ttk.Radiobutton(
            control_frame,
            text="Live Speak (coming soon)",
            variable=self.mode_var,
            value="live",
            state="disabled"
        ).grid(row=2, column=1, sticky="w", pady=5)

        # Save mode – active
        ttk.Radiobutton(
            control_frame,
            text="Save to MP3 (auto filename)",
            variable=self.mode_var,
            value="save"
        ).grid(row=3, column=1, sticky="w", pady=5)

        # Action buttons
        btn_frame = tk.Frame(self.scrollable_frame, bg=WINDOW_BG)  # noqa: F405
        btn_frame.pack(pady=15)

        self.start_btn = ttk.Button(btn_frame, text="▶️ Start", command=self.start_action)
        self.start_btn.pack(side="left", padx=8)

        self.pause_btn = ttk.Button(btn_frame, text="⏸️ Pause", command=self.toggle_pause, state="disabled")
        self.pause_btn.pack(side="left", padx=8)

        self.stop_btn = ttk.Button(btn_frame, text="⏹️ Stop", command=self.stop_action, state="disabled")
        self.stop_btn.pack(side="left", padx=8)

        ttk.Button(btn_frame, text="Clear", command=self.clear_all).pack(side="left", padx=8)

        # Progress bar & status
        self.progress = ttk.Progressbar(
            self.scrollable_frame, orient="horizontal", length=PROGRESS_LENGTH, mode="determinate"  # noqa: F405
        )
        self.progress.pack(pady=8, padx=15, fill="x")

        self.status_var = tk.StringVar(value="Ready - Load a document then click Start")
        tk.Label(
            self.scrollable_frame, textvariable=self.status_var,
            font=(FONT_FAMILY, 10)  # noqa: F405
        ).pack(pady=8)

    def load_voices(self):
        self.voices = get_available_voices()
        names = [f"{i}: {v.name}" for i, v in enumerate(self.voices)]
        self.voice_combo['values'] = names
        if names:
            self.voice_combo.current(0)

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=SUPPORTED_FORMATS)  # noqa: F405
        if path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, path)

    def load_file(self):
        path_str = self.file_entry.get().strip()
        if not path_str:
            messagebox.showwarning("Warning", "Please select a file first!")
            return

        self.file_path = Path(path_str)
        if not self.file_path.exists():
            messagebox.showerror("Error", "File not found!")
            return

        self.status_var.set(f"Loading {self.file_path.name}...")
        self.root.update_idletasks()

        self.full_text = extract_text(self.file_path)

        if self.full_text.startswith(("Error", "Unsupported")):
            messagebox.showerror("Error", self.full_text)
            self.status_var.set("Failed to load document")
            return

        self.preview_text.delete(1.0, tk.END)
        preview = self.full_text[:800] + ("..." if len(self.full_text) > 800 else "")
        self.preview_text.insert(tk.END, preview)

        self.status_var.set(f"✅ Loaded: {self.file_path.name}  |  {len(self.full_text):,} characters")

    def start_action(self):
        if not self.full_text:
            messagebox.showwarning("Warning", "Please load a document first!")
            return

        mode = self.mode_var.get()
        rate = self.speed_var.get()

        if self.voice_combo.current() >= 0:
            idx = self.voice_combo.current()
            self.current_voice_id = self.voices[idx].id if idx < len(self.voices) else None

        self.start_btn.config(state="disabled")

        if mode == "save":
            self.save_to_mp3(rate)
        # Live mode is disabled / coming soon

    def save_to_mp3(self, rate: int):
        output_path = create_auto_mp3_filename(self.file_path)

        def thread_func():
            try:
                self.status_var.set(f"🔄 Saving {output_path.name}...")
                self.progress['value'] = 10
                self.root.update_idletasks()

                save_text_to_mp3(
                    text=self.full_text,
                    output_path=output_path,
                    rate=rate,
                    voice_id=self.current_voice_id
                )

                self.progress['value'] = 100
                self.status_var.set(f"✅ Saved: {output_path.name}")
                messagebox.showinfo("Success", f"MP3 saved successfully!\n\n{output_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save MP3:\n{str(e)}")
                self.status_var.set("❌ Save failed")
            finally:
                self.finish_action()

        self.speaking_thread = threading.Thread(target=thread_func, daemon=True)
        self.speaking_thread.start()

    def toggle_pause(self):
        pass  # disabled – live mode coming soon

    def stop_action(self):
        pass  # disabled – live mode coming soon

    def finish_action(self):
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self.stop_btn.config(state="disabled")
        self.progress['value'] = 0

    def clear_all(self):
        self.file_entry.delete(0, tk.END)
        self.preview_text.delete(1.0, tk.END)
        self.full_text = ""
        self.status_var.set("Ready - Load a document then click Start")


if __name__ == "__main__":
    # This file should NOT be run directly – use main.py
    raise RuntimeError("Run the application using main.py")