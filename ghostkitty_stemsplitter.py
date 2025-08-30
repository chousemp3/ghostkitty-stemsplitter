#!/usr/bin/env python3
"""
🐱‍👻 GhostKitty StemSplitter - Enhanced GUI Version
A user-friendly graphical interface for audio stem separation with bitcrush aesthetics
"""

import math
import os
import random
import sys
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

# Add the current directory to Python path to import ghostkitty
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ghostkitty import GhostKittyStemSplitter
except ImportError as e:
    print(f"Error importing GhostKittyStemSplitter: {e}")
    sys.exit(1)


class BitcrushVisualizer:
    """Animated bitcrush-style visualizer for the GUI"""

    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.is_running = False
        self.particles = []
        self.waveform = []
        self.colors = ["#ff006e", "#fb5607", "#ffbe0b", "#8338ec", "#3a86ff", "#06ffa5"]
        self.ghost_eyes = {"x": width // 2, "y": height // 2 - 40, "blink": False}

        # Create initial waveform points
        for i in range(0, width, 8):
            self.waveform.append(
                {
                    "x": i,
                    "y": height // 2,
                    "target_y": height // 2,
                    "phase": random.uniform(0, math.pi * 2),
                }
            )

        # Create particles
        for _ in range(30):
            self.particles.append(
                {
                    "x": random.randint(0, width),
                    "y": random.randint(0, height),
                    "vx": random.uniform(-2, 2),
                    "vy": random.uniform(-2, 2),
                    "color": random.choice(self.colors),
                    "size": random.randint(2, 6),
                    "life": random.uniform(0.5, 1.0),
                }
            )

    def start_animation(self):
        """Start the animation loop"""
        self.is_running = True
        self.animate()

    def stop_animation(self):
        """Stop the animation"""
        self.is_running = False

    def animate(self):
        """Main animation loop"""
        if not self.is_running:
            return

        self.canvas.delete("all")

        # Draw grid background
        self.draw_grid()

        # Draw animated waveform
        self.draw_waveform()

        # Draw particles
        self.draw_particles()

        # Draw ghost kitty
        self.draw_ghost_kitty()

        # Draw bitcrush effects
        self.draw_bitcrush_effects()

        # Schedule next frame
        self.canvas.after(50, self.animate)

    def draw_grid(self):
        """Draw cyberpunk grid background"""
        grid_size = 20

        # Vertical lines
        for x in range(0, self.width, grid_size):
            alpha = random.randint(10, 30)
            color = (
                f"#{alpha:02x}{alpha // 2:02x}{alpha * 2:02x}"
                if alpha * 2 <= 255
                else f"#{alpha:02x}{alpha // 2:02x}ff"
            )
            self.canvas.create_line(x, 0, x, self.height, fill=color, width=1)

        # Horizontal lines
        for y in range(0, self.height, grid_size):
            alpha = random.randint(10, 30)
            color = (
                f"#{alpha:02x}{alpha // 2:02x}{alpha * 2:02x}"
                if alpha * 2 <= 255
                else f"#{alpha:02x}{alpha // 2:02x}ff"
            )
            self.canvas.create_line(0, y, self.width, y, fill=color, width=1)

    def draw_waveform(self):
        """Draw animated waveform"""
        points = []
        time_offset = time.time() * 3

        for i, point in enumerate(self.waveform):
            # Calculate wave height based on sine wave
            wave_height = math.sin(point["phase"] + time_offset + i * 0.1) * 30
            point["target_y"] = self.height // 2 + wave_height

            # Smooth interpolation to target
            point["y"] += (point["target_y"] - point["y"]) * 0.1

            points.extend([point["x"], point["y"]])

        if len(points) >= 4:
            # Draw glow effect (background layers)
            self.canvas.create_line(points, fill="#330022", width=16, smooth=True)
            self.canvas.create_line(points, fill="#660044", width=10, smooth=True)
            self.canvas.create_line(points, fill="#990066", width=6, smooth=True)

            # Draw main waveform
            self.canvas.create_line(points, fill="#ff006e", width=3, smooth=True)

    def draw_particles(self):
        """Draw floating particles"""
        for particle in self.particles:
            # Update position
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]

            # Wrap around screen
            if particle["x"] < 0:
                particle["x"] = self.width
            elif particle["x"] > self.width:
                particle["x"] = 0

            if particle["y"] < 0:
                particle["y"] = self.height
            elif particle["y"] > self.height:
                particle["y"] = 0

            # Draw particle with glow
            size = particle["size"]
            x, y = particle["x"], particle["y"]

            # Outer glow (darker version of color)
            glow_color = self.darken_color(particle["color"])
            self.canvas.create_oval(
                x - size * 2,
                y - size * 2,
                x + size * 2,
                y + size * 2,
                fill=glow_color,
                outline="",
            )

            # Inner particle
            self.canvas.create_oval(
                x - size,
                y - size,
                x + size,
                y + size,
                fill=particle["color"],
                outline="",
            )

    def darken_color(self, color):
        """Convert a color to a darker version for glow effects"""
        color_map = {
            "#ff006e": "#440022",
            "#fb5607": "#441100",
            "#ffbe0b": "#442200",
            "#8338ec": "#220844",
            "#3a86ff": "#002244",
            "#06ffa5": "#002244",
        }
        return color_map.get(color, "#222222")

    def draw_ghost_kitty(self):
        """Draw animated ghost kitty face"""
        x, y = self.ghost_eyes["x"], self.ghost_eyes["y"]

        # Randomly blink
        if random.random() < 0.02:
            self.ghost_eyes["blink"] = not self.ghost_eyes["blink"]

        # Ghost body (glowing layers)
        self.canvas.create_oval(
            x - 70, y - 70, x + 70, y + 70, fill="#001122", outline=""
        )
        self.canvas.create_oval(
            x - 60, y - 60, x + 60, y + 60, fill="#002244", outline=""
        )
        self.canvas.create_oval(
            x - 50, y - 50, x + 50, y + 50, fill="#003366", outline=""
        )

        # Eyes
        eye_size = 8 if not self.ghost_eyes["blink"] else 2

        # Left eye
        self.canvas.create_oval(
            x - 15, y - eye_size, x - 5, y + eye_size, fill="#ff006e", outline=""
        )

        # Right eye
        self.canvas.create_oval(
            x + 5, y - eye_size, x + 15, y + eye_size, fill="#ff006e", outline=""
        )

        # Mouth (small smile)
        if not self.ghost_eyes["blink"]:
            self.canvas.create_arc(
                x - 10,
                y + 5,
                x + 10,
                y + 20,
                start=0,
                extent=180,
                outline="#ff006e",
                width=2,
                style="arc",
            )

    def draw_bitcrush_effects(self):
        """Draw digital distortion effects"""
        # Random digital noise squares
        for _ in range(5):
            if random.random() < 0.3:
                x = random.randint(0, self.width - 20)
                y = random.randint(0, self.height - 20)
                size = random.randint(5, 15)
                color = random.choice(
                    ["#330022", "#220033", "#003322", "#332200", "#002233"]
                )

                self.canvas.create_rectangle(
                    x, y, x + size, y + size, fill=color, outline=""
                )

        # Glitch lines
        for _ in range(3):
            if random.random() < 0.1:
                y = random.randint(0, self.height)
                width = random.randint(50, 200)
                x = random.randint(0, self.width - width)

                self.canvas.create_rectangle(
                    x, y, x + width, y + 2, fill="#660022", outline=""
                )


class GhostKittyStemSplitterGUI:
    """Enhanced GUI for GhostKitty StemSplitter with cool visuals"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🐱‍👻 GhostKitty StemSplitter - Cyberpunk Edition")
        self.root.geometry("900x700")

        # Dark cyberpunk theme
        self.colors = {
            "bg": "#0a0a0a",
            "bg_secondary": "#1a1a2e",
            "bg_tertiary": "#16213e",
            "accent": "#ff006e",
            "accent2": "#3a86ff",
            "accent3": "#06ffa5",
            "text": "#ffffff",
            "text_dim": "#a0a0a0",
            "button": "#ff006e",
            "button_hover": "#ff3385",
        }

        self.root.configure(bg=self.colors["bg"])

        # Configure styles
        self.setup_styles()

        # Variables
        self.input_file_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.model_var = tk.StringVar(value="htdemucs")
        self.device_var = tk.StringVar(value="auto")

        # Splitter instance
        self.splitter = None

        # Animation state
        self.is_processing = False

        self.create_widgets()

    def setup_styles(self):
        """Configure ttk styles for dark theme"""
        style = ttk.Style()

        # Configure root window options for better widget styling
        self.root.option_add("*TCombobox*Listbox.selectBackground", "#ff006e")
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")
        self.root.option_add("*TCombobox*Listbox.background", "#2b2b2b")
        self.root.option_add("*TCombobox*Listbox.foreground", "#ffffff")

        # Configure Combobox for better readability
        style.theme_use("clam")

        style.configure(
            "Dark.TCombobox",
            fieldbackground="#2b2b2b",  # Dark background
            background="#2b2b2b",  # Dark background
            foreground="#ffffff",  # White text
            borderwidth=2,
            relief="flat",
            selectbackground="#ff006e",  # Pink selection
            selectforeground="#ffffff",  # White selected text
            arrowcolor="#ff006e",
        )  # Pink arrow

        # Configure the dropdown listbox
        style.map(
            "Dark.TCombobox",
            fieldbackground=[("readonly", "#2b2b2b")],
            selectbackground=[("readonly", "#ff006e")],
            selectforeground=[("readonly", "#ffffff")],
            foreground=[("readonly", "#ffffff")],
            arrowcolor=[("readonly", "#ff006e")],
        )

        # Configure Progressbar
        style.configure(
            "Cyber.Horizontal.TProgressbar",
            background=self.colors["accent"],
            troughcolor=self.colors["bg_secondary"],
            borderwidth=0,
            lightcolor=self.colors["accent"],
            darkcolor=self.colors["accent"],
        )

    def create_widgets(self):
        """Create and arrange GUI widgets with cyberpunk styling"""

        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors["bg"])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header with animated visualizer
        header_frame = tk.Frame(main_container, bg=self.colors["bg"])
        header_frame.pack(fill="x", pady=(0, 20))

        # Visualizer canvas
        self.viz_canvas = tk.Canvas(
            header_frame,
            width=860,
            height=200,
            bg=self.colors["bg"],
            highlightthickness=0,
        )
        self.viz_canvas.pack()

        # Initialize visualizer
        self.visualizer = BitcrushVisualizer(self.viz_canvas, 860, 200)
        self.visualizer.start_animation()

        # Title overlay on visualizer
        self.viz_canvas.create_text(
            430,
            50,
            text="🐱‍👻 GHOSTKITTY STEMSPLITTER",
            font=("Courier New", 24, "bold"),
            fill=self.colors["accent"],
            anchor="center",
        )

        self.viz_canvas.create_text(
            430,
            80,
            text="CYBERPUNK EDITION • SPLIT • REMIX • DOMINATE",
            font=("Courier New", 10, "bold"),
            fill=self.colors["accent3"],
            anchor="center",
        )

        # Content area
        content_frame = tk.Frame(
            main_container, bg=self.colors["bg_secondary"], relief="raised", bd=2
        )
        content_frame.pack(fill="both", expand=True, pady=10)

        # Inner content with padding
        inner_frame = tk.Frame(content_frame, bg=self.colors["bg_secondary"])
        inner_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Input file selection
        self.create_file_section(
            inner_frame,
            "📁 SELECT AUDIO FILE",
            self.input_file_var,
            self.browse_input_file,
        )

        # Output directory selection
        self.create_file_section(
            inner_frame,
            "💾 OUTPUT DIRECTORY [OPTIONAL]",
            self.output_dir_var,
            self.browse_output_dir,
        )

        # Settings section
        settings_frame = self.create_section_frame(inner_frame, "⚙️ CYBERPUNK SETTINGS")

        # Model and device in a grid
        settings_grid = tk.Frame(settings_frame, bg=self.colors["bg_secondary"])
        settings_grid.pack(fill="x", padx=20, pady=10)

        # Left column - Model
        model_frame = tk.Frame(settings_grid, bg=self.colors["bg_secondary"])
        model_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.create_cyber_label(model_frame, "AI MODEL:")
        model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=["htdemucs", "htdemucs_ft", "mdx_extra"],
            state="readonly",
            style="Dark.TCombobox",
            font=("Courier New", 11, "bold"),
            width=15,
        )
        model_combo.pack(fill="x", pady=(5, 0))

        # Right column - Device
        device_frame = tk.Frame(settings_grid, bg=self.colors["bg_secondary"])
        device_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))

        self.create_cyber_label(device_frame, "DEVICE:")
        device_combo = ttk.Combobox(
            device_frame,
            textvariable=self.device_var,
            values=["auto", "cpu", "cuda", "mps"],
            state="readonly",
            style="Dark.TCombobox",
            font=("Courier New", 11, "bold"),
            width=15,
        )
        device_combo.pack(fill="x", pady=(5, 0))

        # Progress section
        progress_frame = self.create_section_frame(inner_frame, "🔄 PROCESSING STATUS")

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=600,
            mode="indeterminate",
            style="Cyber.Horizontal.TProgressbar",
        )
        self.progress_bar.pack(pady=20)

        # Status display
        self.status_label = tk.Label(
            progress_frame,
            text="SYSTEM READY • AWAITING AUDIO INPUT",
            font=("Courier New", 12, "bold"),
            fg=self.colors["accent3"],
            bg=self.colors["bg_secondary"],
        )
        self.status_label.pack(pady=(0, 20))

        # Action buttons
        button_frame = tk.Frame(inner_frame, bg=self.colors["bg_secondary"])
        button_frame.pack(pady=20)

        # Split button
        self.split_button = self.create_cyber_button(
            button_frame, "🐱‍👻 INITIATE STEM SPLIT", self.start_splitting, primary=True
        )
        self.split_button.pack(side="left", padx=10)

        # Exit button
        self.create_cyber_button(
            button_frame, "❌ DISCONNECT", self.root.quit, primary=False
        ).pack(side="right", padx=10)

        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_section_frame(self, parent, title):
        """Create a styled section frame"""
        section = tk.LabelFrame(
            parent,
            text=title,
            font=("Courier New", 10, "bold"),
            fg=self.colors["accent"],
            bg=self.colors["bg_secondary"],
            relief="flat",
            bd=2,
        )
        section.pack(fill="x", pady=10)
        return section

    def create_file_section(self, parent, title, var, browse_func):
        """Create a file selection section"""
        section = self.create_section_frame(parent, title)

        file_frame = tk.Frame(section, bg=self.colors["bg_secondary"])
        file_frame.pack(fill="x", padx=20, pady=10)

        # Entry field
        entry = tk.Entry(
            file_frame,
            textvariable=var,
            font=("Courier New", 10),
            bg=self.colors["bg_tertiary"],
            fg=self.colors["text"],
            insertbackground=self.colors["accent"],
            relief="flat",
            bd=5,
        )
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Browse button
        self.create_cyber_button(file_frame, "BROWSE", browse_func, small=True).pack(
            side="right"
        )

    def create_cyber_label(self, parent, text):
        """Create a cyberpunk-styled label"""
        label = tk.Label(
            parent,
            text=text,
            font=("Courier New", 9, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg_secondary"],
        )
        label.pack(anchor="w")
        return label

    def create_cyber_button(self, parent, text, command, primary=True, small=False):
        """Create a cyberpunk-styled button"""
        if primary:
            bg_color = self.colors["button"]
            fg_color = self.colors["text"]
        else:
            bg_color = self.colors["bg_tertiary"]
            fg_color = self.colors["text_dim"]

        font_size = 8 if small else 11
        pad_x = 15 if small else 30
        pad_y = 5 if small else 12

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            font=("Courier New", font_size, "bold"),
            relief="flat",
            bd=0,
            padx=pad_x,
            pady=pad_y,
            cursor="hand2",
        )

        # Hover effects
        def on_enter(e):
            button.config(
                bg=(
                    self.colors["button_hover"]
                    if primary
                    else self.colors["bg_tertiary"]
                )
            )

        def on_leave(e):
            button.config(bg=bg_color)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        return button

    def browse_input_file(self):
        """Browse for input audio file"""
        filetypes = [
            ("Audio Files", "*.mp3 *.wav *.flac *.m4a *.aac *.ogg"),
            ("MP3 Files", "*.mp3"),
            ("WAV Files", "*.wav"),
            ("FLAC Files", "*.flac"),
            ("All Files", "*.*"),
        ]

        filename = filedialog.askopenfilename(
            title="SELECT AUDIO FILE FOR PROCESSING", filetypes=filetypes
        )

        if filename:
            self.input_file_var.set(filename)
            self.update_status(
                "AUDIO FILE LOADED • READY FOR PROCESSING", self.colors["accent3"]
            )

    def browse_output_dir(self):
        """Browse for output directory"""
        dirname = filedialog.askdirectory(title="SELECT OUTPUT DIRECTORY")
        if dirname:
            self.output_dir_var.set(dirname)
            self.update_status("OUTPUT DIRECTORY SET", self.colors["accent3"])

    def update_status(self, message: str, color: str = None):
        """Update status label with cyberpunk styling"""
        if color is None:
            color = self.colors["text_dim"]

        self.status_label.config(text=message, fg=color)
        self.root.update()

        # Add some visual feedback
        if "ERROR" in message.upper():
            self.flash_screen("#ff0040", 100)
        elif "SUCCESS" in message.upper():
            self.flash_screen("#06ffa5", 150)

    def flash_screen(self, color, duration):
        """Flash the screen with a color for visual feedback"""
        original_bg = self.root.cget("bg")
        self.root.configure(bg=color)
        self.root.after(duration, lambda: self.root.configure(bg=original_bg))

    def start_splitting(self):
        """Start the audio splitting process in a separate thread"""
        input_file = self.input_file_var.get().strip()

        if not input_file:
            self.update_status("ERROR • NO AUDIO FILE SELECTED", "#ff0040")
            messagebox.showerror(
                "SYSTEM ERROR", "Please select an audio file for processing!"
            )
            return

        if not Path(input_file).exists():
            self.update_status("ERROR • FILE NOT FOUND", "#ff0040")
            messagebox.showerror(
                "SYSTEM ERROR", "Selected file does not exist in the system!"
            )
            return

        # Visual feedback
        self.is_processing = True
        self.split_button.config(state="disabled", text="🔄 PROCESSING...")
        self.progress_bar.start()

        # Update visualizer for processing mode
        self.update_status("INITIALIZING AI SYSTEMS...", self.colors["accent"])

        # Start splitting in a separate thread
        thread = threading.Thread(target=self.split_audio_thread)
        thread.daemon = True
        thread.start()

    def split_audio_thread(self):
        """Run audio splitting in a separate thread"""
        try:
            input_path = Path(self.input_file_var.get().strip())
            output_dir = None

            if self.output_dir_var.get().strip():
                output_dir = Path(self.output_dir_var.get().strip())

            # Determine device
            device = None if self.device_var.get() == "auto" else self.device_var.get()

            self.update_status("LOADING NEURAL NETWORKS... 🤖", self.colors["accent"])

            # Create splitter
            self.splitter = GhostKittyStemSplitter(
                model_name=self.model_var.get(), device=device
            )

            self.update_status(
                "AI MODEL LOADED • BEGINNING SEPARATION...", self.colors["accent2"]
            )

            # Split the audio
            success = self.splitter.split_audio(input_path, output_dir)

            if success:
                self.update_status(
                    "✅ MISSION COMPLETE • STEMS EXTRACTED SUCCESSFULLY", "#06ffa5"
                )
                self.flash_screen("#06ffa5", 200)

                messagebox.showinfo(
                    "MISSION COMPLETE",
                    "🎉 AUDIO SUCCESSFULLY SEPARATED INTO 4 STEMS!\n\n"
                    "EXTRACTED COMPONENTS:\n"
                    "🎤 VOCALS.WAV\n"
                    "🥁 DRUMS.WAV\n"
                    "🎸 BASS.WAV\n"
                    "🎵 OTHER.WAV\n\n"
                    "STEMS ARE READY FOR REMIX OPERATIONS! �",
                )
            else:
                self.update_status(
                    "❌ PROCESSING FAILED • CHECK SYSTEM LOGS", "#ff0040"
                )
                self.flash_screen("#ff0040", 200)
                messagebox.showerror(
                    "SYSTEM ERROR",
                    "Failed to process audio file.\nCheck console for diagnostic information.",
                )

        except Exception as e:
            self.update_status(f"❌ CRITICAL ERROR: {str(e)}", "#ff0040")
            self.flash_screen("#ff0040", 300)
            messagebox.showerror(
                "CRITICAL SYSTEM ERROR", f"A critical error occurred:\n{str(e)}"
            )

        finally:
            # Reset UI state
            self.is_processing = False
            self.progress_bar.stop()
            self.split_button.config(state="normal", text="🐱‍👻 INITIATE STEM SPLIT")

    def on_closing(self):
        """Handle window close event"""
        if self.visualizer:
            self.visualizer.stop_animation()
        self.root.destroy()

    def run(self):
        """Run the GUI application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()


if __name__ == "__main__":
    app = GhostKittyStemSplitterGUI()
    app.run()
