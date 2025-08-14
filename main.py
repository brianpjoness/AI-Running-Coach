import tkinter as tk
from tkinter import ttk
import time
import threading
import cv2
from PIL import Image, ImageTk
import os
from datetime import datetime

class Timer:
    def __init__(self, parent, timer_id, parent_app):
        self.timer_id = timer_id
        self.parent = parent
        self.parent_app = parent_app
        
        # Timer state
        self.is_running = False
        self.start_time = 0
        self.elapsed_time = 0
        
        # Split timer state
        self.split_start_time = 0
        self.split_elapsed_time = 0
        self.is_split_running = False
        self.splits = []  # List to store split times
        
        # Create GUI elements
        self.setup_ui()
        
    def setup_ui(self):
        # Timer frame - minimalistic design
        self.timer_frame = ttk.Frame(self.parent, relief="solid", borderwidth=1)
        
        # Header with timer number, name input, and remove button
        header_frame = ttk.Frame(self.timer_frame)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(2, 0))
        
        # Timer number label
        timer_label = ttk.Label(header_frame, text=f"#{self.timer_id}", font=("Arial", 8, "bold"))
        timer_label.grid(row=0, column=0, padx=2, sticky=(tk.W))
        
        # Name input field
        self.name_var = tk.StringVar(value=f"Timer {self.timer_id}")
        self.name_entry = ttk.Entry(header_frame, textvariable=self.name_var, width=12, font=("Arial", 8))
        self.name_entry.grid(row=0, column=1, padx=2, sticky=(tk.W, tk.E))
        
        # Remove button (X) in the top-right corner
        self.remove_button = ttk.Button(header_frame, text="✕", command=self.remove_timer, width=2)
        self.remove_button.grid(row=0, column=2, padx=2, sticky=(tk.E))
        
        # Configure header frame weights
        header_frame.columnconfigure(1, weight=1)  # Name field expands
        
        # Main timer display (larger, prominent)
        self.time_label = ttk.Label(self.timer_frame, text="00:00.000", font=("Arial", 18, "bold"))
        self.time_label.grid(row=1, column=0, columnspan=3, pady=2)
        
        # Split timer display (smaller, below main)
        self.split_time_label = ttk.Label(self.timer_frame, text="00:00.000", font=("Arial", 10))
        self.split_time_label.grid(row=2, column=0, columnspan=3, pady=(0, 2))
        
        # Control buttons (compact horizontal row)
        button_frame = ttk.Frame(self.timer_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=2)
        
        # Start/Stop button
        self.start_button = ttk.Button(button_frame, text="▶", command=self.toggle_timer, width=3)
        self.start_button.grid(row=0, column=0, padx=1)
        
        # Split button
        self.split_button = ttk.Button(button_frame, text="⏱", command=self.toggle_split, state="disabled", width=3)
        self.split_button.grid(row=0, column=1, padx=1)
        
        # Reset button
        self.reset_button = ttk.Button(button_frame, text="↺", command=self.reset_timer, width=3)
        self.reset_button.grid(row=0, column=2, padx=1)
        
        # Configure grid weights
        self.timer_frame.columnconfigure(0, weight=1)
        self.timer_frame.columnconfigure(1, weight=1)
        self.timer_frame.columnconfigure(2, weight=1)
        
        # Bind name change event
        self.name_var.trace('w', self.on_name_change)
        
    def on_name_change(self, *args):
        """Handle name changes and update split history"""
        self.parent_app.update_split_history()
        
    def get_display_name(self):
        """Get the timer name with truncation for display"""
        name = self.name_var.get().strip()
        if not name:
            name = f"Timer {self.timer_id}"
        
        # Truncate if too long (max 12 characters to fit column width)
        if len(name) > 12:
            return name[:9] + "..."
        return name
        
    def toggle_timer(self):
        if not self.is_running:
            self.start_timer()
        else:
            self.stop_timer()
            
    def start_timer(self):
        self.is_running = True
        self.start_time = time.perf_counter() - self.elapsed_time
        self.start_button.config(text="⏸")
        self.split_button.config(state="normal")
        self.update_timer()
        
    def stop_timer(self):
        self.is_running = False
        self.elapsed_time = time.perf_counter() - self.start_time
        self.start_button.config(text="▶")
        self.split_button.config(state="disabled")
        
        # Stop split timer if it's running
        if self.is_split_running:
            self.stop_split()
            
    def toggle_split(self):
        if not self.is_split_running:
            self.start_split()
        else:
            self.stop_split()
            self.start_split()  # Start next split immediately
            
    def start_split(self):
        self.is_split_running = True
        self.split_start_time = time.perf_counter() - self.split_elapsed_time
        self.split_button.config(text="⏱")
        self.update_split_timer()
        
    def stop_split(self):
        if self.is_split_running:
            self.is_split_running = False
            split_time = time.perf_counter() - self.split_start_time
            self.splits.append(split_time)
            self.parent_app.update_split_history()  # Update the main split history
            self.split_elapsed_time = 0  # Reset for next split
            self.split_time_label.config(text="00:00.000")
        
    def reset_timer(self):
        self.is_running = False
        self.elapsed_time = 0
        self.start_button.config(text="▶")
        self.time_label.config(text="00:00.000")
        
        # Reset split timer
        self.is_split_running = False
        self.split_elapsed_time = 0
        self.split_time_label.config(text="00:00.000")
        self.split_button.config(text="⏱", state="disabled")
        
        # Clear split history
        self.splits = []
        self.parent_app.update_split_history()
        
    def update_timer(self):
        if self.is_running:
            current_time = time.perf_counter() - self.start_time
            self.update_display(current_time)
            # Schedule next update in 10ms (100Hz for smooth display)
            self.parent_app.root.after(10, self.update_timer)
            
    def update_split_timer(self):
        if self.is_split_running and self.is_running:
            current_split_time = time.perf_counter() - self.split_start_time
            self.update_split_display(current_split_time)
            # Schedule next update in 10ms (100Hz for smooth display)
            self.parent_app.root.after(10, self.update_split_timer)
            
    def update_display(self, elapsed_seconds):
        """Update the timer display with MM:SS.mmm format"""
        minutes = int(elapsed_seconds // 60)
        seconds = int(elapsed_seconds % 60)
        milliseconds = int((elapsed_seconds % 1) * 1000)
        
        time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        self.time_label.config(text=time_str)
        
    def update_split_display(self, elapsed_seconds):
        """Update the split timer display with MM:SS.mmm format"""
        minutes = int(elapsed_seconds // 60)
        seconds = int(elapsed_seconds % 60)
        milliseconds = int((elapsed_seconds % 1) * 1000)
        
        time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        self.split_time_label.config(text=time_str)

    def remove_timer(self):
        """Remove this timer from the application"""
        # Stop the timer if it's running
        if self.is_running:
            self.stop_timer()
        
        # Remove from parent app
        self.parent_app.remove_timer(self)

class MultiTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi Timer with Video Recording")
        self.root.geometry("1200x800")
        
        # Timer management
        self.timers = []
        self.max_timers = 10
        
        # Video recorder
        self.video_recorder = VideoRecorder(self)
        
        # Create GUI elements
        self.setup_ui()
        
        # Add the first timer
        self.add_timer()
        
        # Bind keyboard shortcuts
        self.root.bind('<KeyRelease>', self.on_key_release)
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Top controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky=(tk.W, tk.E))
        
        # Add timer button
        self.add_button = ttk.Button(controls_frame, text="+", command=self.add_timer, width=3)
        self.add_button.grid(row=0, column=0, padx=(0, 10))
        
        # Start all timers button
        self.start_all_button = ttk.Button(controls_frame, text="▶▶", command=self.start_all_timers, width=5)
        self.start_all_button.grid(row=0, column=1, padx=(0, 10))
        
        # Timer count label
        self.timer_count_label = ttk.Label(controls_frame, text="Timers: 1/10")
        self.timer_count_label.grid(row=0, column=2, padx=(0, 20))
        
        # Video controls
        video_controls_frame = ttk.LabelFrame(controls_frame, text="Video Recording", padding="5")
        video_controls_frame.grid(row=0, column=3, padx=(0, 10))
        
        # Video recording button
        self.record_button = ttk.Button(video_controls_frame, text="🔴", command=self.toggle_recording, width=3)
        self.record_button.grid(row=0, column=0, padx=2)
        
        # Recording status label
        self.recording_status = ttk.Label(video_controls_frame, text="●", foreground="red")
        self.recording_status.grid(row=0, column=1, padx=10)
        
        # Save button
        self.save_button = ttk.Button(video_controls_frame, text="💾", command=self.save_session, width=3)
        self.save_button.grid(row=0, column=2, padx=2)
        
        # Create left panel for timers
        left_panel = ttk.Frame(main_frame)
        left_panel.grid(row=1, column=0, pady=(0, 5), sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Create a canvas with scrollbar for timers
        canvas_frame = ttk.Frame(left_panel)
        canvas_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.canvas = tk.Canvas(canvas_frame, height=400)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.timers_frame = ttk.Frame(self.canvas)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Create window in canvas for timers frame
        self.canvas_window = self.canvas.create_window((0, 0), window=self.timers_frame, anchor="nw")
        
        # Create right panel for video preview
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=1, column=1, pady=(0, 5), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Video preview frame
        preview_frame = ttk.LabelFrame(right_panel, text="Video Preview", padding="5")
        preview_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Video preview label
        self.preview_label = ttk.Label(preview_frame, text="No Video Feed", relief="solid", borderwidth=1)
        self.preview_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Split history display (spans both columns)
        history_frame = ttk.LabelFrame(main_frame, text="Split History", padding="3")
        history_frame.grid(row=2, column=0, columnspan=2, pady=(5, 0), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create a compact scrollable text widget for split history
        self.split_history = tk.Text(history_frame, height=8, width=120, font=("Consolas", 8))
        history_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.split_history.yview)
        self.split_history.configure(yscrollcommand=history_scrollbar.set)
        
        self.split_history.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        history_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=2)  # Timers panel
        main_frame.columnconfigure(1, weight=1)  # Video panel
        main_frame.rowconfigure(1, weight=1)
        left_panel.columnconfigure(0, weight=1)
        left_panel.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        
        # Bind canvas resize
        self.timers_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
    def toggle_recording(self):
        """Toggle video recording on/off"""
        if not self.video_recorder.is_recording:
            self.video_recorder.start_recording()
            self.record_button.config(text="⏹")
            self.recording_status.config(text="●", foreground="red")
        else:
            self.video_recorder.stop_recording()
            self.record_button.config(text="🔴")
            self.recording_status.config(text="●", foreground="gray")
    
    def start_all_timers(self):
        """Start all timers simultaneously"""
        for timer in self.timers:
            if not timer.is_running:
                timer.start_timer()
    
    def reset_all_timers(self):
        """Reset all timers to their initial state"""
        for timer in self.timers:
            timer.reset_timer()
    
    def save_session(self):
        """Save the current session including recording and split data"""
        import json
        from datetime import datetime
        
        # Create sessions directory if it doesn't exist
        sessions_dir = "sessions"
        if not os.path.exists(sessions_dir):
            os.makedirs(sessions_dir)
        
        # Generate timestamp for the session
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Stop recording if it's currently active
        recording_saved = False
        if self.video_recorder.is_recording:
            self.video_recorder.stop_recording()
            self.record_button.config(text="🔴")
            self.recording_status.config(text="●", foreground="gray")
            recording_saved = True
            print(f"Recording stopped and saved for session: {timestamp}")
        
        # Prepare split data
        session_data = {
            "timestamp": timestamp,
            "recording_saved": recording_saved,
            "timers": []
        }
        
        # Collect data from each timer
        for timer in self.timers:
            timer_data = {
                "name": timer.name_var.get().strip(),
                "timer_id": timer.timer_id,
                "splits": []
            }
            
            # Add split times
            for i, split_time in enumerate(timer.splits, 1):
                minutes = int(split_time // 60)
                seconds = int(split_time % 60)
                milliseconds = int((split_time % 1) * 1000)
                time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
                
                timer_data["splits"].append({
                    "split_number": i,
                    "time_seconds": split_time,
                    "time_formatted": time_str
                })
            
            session_data["timers"].append(timer_data)
        
        # Save session data to JSON file
        session_file = os.path.join(sessions_dir, f"session_{timestamp}.json")
        try:
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            print(f"Session data saved to: {session_file}")
            
            # Show success message
            self.show_save_message(f"Session saved successfully!\nRecording: {'Yes' if recording_saved else 'No'}\nData: {session_file}")
            
        except Exception as e:
            print(f"Error saving session data: {e}")
            self.show_save_message("Error saving session data!")
    
    def show_save_message(self, message):
        """Show a temporary message about the save operation"""
        # Create a simple popup message
        popup = tk.Toplevel(self.root)
        popup.title("Save Status")
        popup.geometry("300x150")
        popup.transient(self.root)
        popup.grab_set()
        
        # Center the popup
        popup.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Add message
        msg_label = ttk.Label(popup, text=message, wraplength=250, justify="center")
        msg_label.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Auto-close after 3 seconds
        popup.after(3000, popup.destroy)
    
    def on_key_release(self, event):
        """Handle keyboard shortcuts"""
        # Don't process shortcuts if focus is in an entry widget (typing timer names)
        focused_widget = self.root.focus_get()
        if isinstance(focused_widget, tk.Entry):
            return
            
        if event.keysym == 'r':
            self.reset_all_timers()
        
    def on_frame_configure(self, event=None):
        """Update canvas scroll region when frame size changes"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_canvas_configure(self, event):
        """Update canvas window width when canvas is resized"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        
    def add_timer(self):
        if len(self.timers) >= self.max_timers:
            return
            
        timer_id = len(self.timers) + 1
        timer = Timer(self.timers_frame, timer_id, self)
        
        # Position the timer in a grid layout (3 columns for better space usage)
        row = (timer_id - 1) // 3
        col = (timer_id - 1) % 3
        
        timer.timer_frame.grid(row=row, column=col, padx=3, pady=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for the timers frame
        self.timers_frame.columnconfigure(col, weight=1)
        self.timers_frame.rowconfigure(row, weight=1)
        
        self.timers.append(timer)
        self.update_timer_count()
        self.update_split_history()
        
        # Disable add button if max reached
        if len(self.timers) >= self.max_timers:
            self.add_button.config(state="disabled")
            
    def update_timer_count(self):
        self.timer_count_label.config(text=f"Timers: {len(self.timers)}/{self.max_timers}")
        
    def update_split_history(self):
        """Update the split history display with columns for each timer"""
        self.split_history.delete(1.0, tk.END)
        
        # Find the maximum number of splits across all timers
        max_splits = max([len(timer.splits) for timer in self.timers]) if self.timers else 0
        
        if max_splits == 0:
            return
            
        # Create header row with fixed column widths
        header = "Split"
        for timer in self.timers:
            display_name = timer.get_display_name()
            # Use fixed width of 12 characters for each column to fit 10 timers
            header += f"{display_name:>12}"
        self.split_history.insert(tk.END, header + "\n")
        self.split_history.insert(tk.END, "-" * len(header) + "\n")
        
        # Create data rows with consistent column widths
        for split_num in range(max_splits):
            row = f"{split_num + 1:>4}"
            for timer in self.timers:
                if split_num < len(timer.splits):
                    split_time = timer.splits[split_num]
                    minutes = int(split_time // 60)
                    seconds = int(split_time % 60)
                    milliseconds = int((split_time % 1) * 1000)
                    time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
                    # Use fixed width of 12 characters to match header
                    row += f"{time_str:>12}"
                else:
                    # Empty cell with same width
                    row += f"{'':>12}"
            self.split_history.insert(tk.END, row + "\n")
            
        self.split_history.see(tk.END)  # Scroll to bottom

    def remove_timer(self, timer_to_remove):
        """Remove a specific timer from the timers list"""
        if timer_to_remove in self.timers:
            # Destroy the timer's GUI elements
            timer_to_remove.timer_frame.destroy()
            
            # Remove from timers list
            self.timers.remove(timer_to_remove)
            
            # Renumber remaining timers
            self.renumber_timers()
            
            # Re-layout timers in the grid
            self.relayout_timers()
            
            # Update UI
            self.update_timer_count()
            self.update_split_history()
            
            # Re-enable add button if it was disabled
            if len(self.timers) < self.max_timers:
                self.add_button.config(state="normal")
                
    def renumber_timers(self):
        """Renumber all timers sequentially starting from 1"""
        for i, timer in enumerate(self.timers, 1):
            timer.timer_id = i
            # Update the timer number label
            for child in timer.timer_frame.winfo_children():
                if isinstance(child, ttk.Frame) and child.winfo_children():
                    # Find the timer label in the header frame
                    for header_child in child.winfo_children():
                        if isinstance(header_child, ttk.Label) and header_child.cget("text").startswith("#"):
                            header_child.config(text=f"#{i}")
                            break
            
            # Update default name if it's still the default
            current_name = timer.name_var.get()
            if current_name.startswith("Timer ") and current_name.split()[-1].isdigit():
                # Only update if it's a default name (Timer X)
                old_num = current_name.split()[-1]
                if old_num.isdigit():
                    timer.name_var.set(f"Timer {i}")
                            
    def relayout_timers(self):
        """Re-layout all timers in the grid after removal"""
        for i, timer in enumerate(self.timers):
            # Calculate new position (3 columns)
            row = i // 3
            col = i % 3
            
            # Move timer to new position
            timer.timer_frame.grid(row=row, column=col, padx=3, pady=3, sticky=(tk.W, tk.E, tk.N, tk.S))

    def on_closing(self):
        """Handle application closing"""
        # Stop video recording if active
        if self.video_recorder.is_recording:
            self.video_recorder.stop_recording()
        
        # Close the application
        self.root.destroy()

class VideoRecorder:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.is_recording = False
        self.cap = None
        self.video_writer = None
        self.recording_thread = None
        self.preview_thread = None
        self.stop_preview = False
        
        # Video settings
        self.fps = 30
        self.frame_width = 640
        self.frame_height = 480
        
        # Create video directory
        self.video_dir = "recordings"
        if not os.path.exists(self.video_dir):
            os.makedirs(self.video_dir)
            
    def start_recording(self):
        """Start video recording"""
        if self.is_recording:
            return
            
        # Initialize camera
        self.cap = cv2.VideoCapture(0)  # Use default webcam
        if not self.cap.isOpened():
            print("Error: Could not open webcam")
            return
            
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        
        # Create video filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.mp4"
        filepath = os.path.join(self.video_dir, filename)
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(filepath, fourcc, self.fps, (self.frame_width, self.frame_height))
        
        self.is_recording = True
        
        # Start recording thread
        self.recording_thread = threading.Thread(target=self._record_video)
        self.recording_thread.daemon = True
        self.recording_thread.start()
        
        # Start preview thread
        self.stop_preview = False
        self.preview_thread = threading.Thread(target=self._update_preview)
        self.preview_thread.daemon = True
        self.preview_thread.start()
        
        print(f"Started recording: {filepath}")
        
    def stop_recording(self):
        """Stop video recording"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        self.stop_preview = True
        
        # Release video writer first to stop recording thread
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        
        # Wait for threads to finish
        if self.recording_thread:
            self.recording_thread.join(timeout=1)
        if self.preview_thread:
            self.preview_thread.join(timeout=1)
            
        # Release camera
        if self.cap:
            self.cap.release()
            self.cap = None
        
        print("Stopped recording")
        
    def _record_video(self):
        """Record video in separate thread"""
        while self.is_recording and self.cap and self.video_writer:
            ret, frame = self.cap.read()
            if ret and self.video_writer is not None:
                # Add timer overlays to the frame only if recording
                frame_with_overlays = self._add_timer_overlays(frame)
                try:
                    self.video_writer.write(frame_with_overlays)
                except:
                    # Video writer was released, stop recording
                    break
            else:
                break
                
    def _update_preview(self):
        """Update video preview in separate thread"""
        while not self.stop_preview and self.cap:
            ret, frame = self.cap.read()
            if ret:
                # Add timer overlays to the preview frame only if recording
                frame_with_overlays = self._add_timer_overlays(frame)
                
                # Convert frame for tkinter
                frame_rgb = cv2.cvtColor(frame_with_overlays, cv2.COLOR_BGR2RGB)
                frame_pil = Image.fromarray(frame_rgb)
                frame_tk = ImageTk.PhotoImage(frame_pil)
                
                # Update preview in main thread
                self.parent_app.root.after(0, self._update_preview_widget, frame_tk)
            else:
                break
                
    def _add_timer_overlays(self, frame):
        """Add timer overlays to the video frame"""
        # Create a copy of the frame to avoid modifying the original
        frame_with_overlays = frame.copy()
        
        # Only add overlays if recording is active
        if not self.is_recording:
            return frame_with_overlays
        
        # Get active timers and their current times
        active_timers = [timer for timer in self.parent_app.timers if timer.is_running]
        
        if not active_timers:
            return frame_with_overlays
            
        # Find the timer with the longest elapsed time
        longest_timer = max(active_timers, key=lambda t: time.perf_counter() - t.start_time)
        
        # Calculate current time for the longest timer
        current_time = time.perf_counter() - longest_timer.start_time
        
        # Format time as MM:SS.mmm
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        milliseconds = int((current_time % 1) * 1000)
        time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        
        # Get timer name
        timer_name = longest_timer.get_display_name()
        
        # Create overlay text
        overlay_text = f"{timer_name}: {time_str}"
        
        # Position for the timer (single overlay)
        overlay_x = 10
        overlay_y = 120  # Moved down to avoid top quarter
        
        # Add text overlay with background
        self._add_text_overlay(frame_with_overlays, overlay_text, overlay_x, overlay_y)
            
        return frame_with_overlays
        
    def _add_text_overlay(self, frame, text, x, y):
        """Add text overlay with background to the frame"""
        # Font settings
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        color = (255, 255, 255)  # White text
        bg_color = (0, 0, 0)     # Black background
        
        # Get text size
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        
        # Calculate background rectangle
        padding = 5
        rect_x1 = x - padding
        rect_y1 = y - text_height - padding
        rect_x2 = x + text_width + padding
        rect_y2 = y + baseline + padding
        
        # Draw background rectangle
        cv2.rectangle(frame, (rect_x1, rect_y1), (rect_x2, rect_y2), bg_color, -1)
        
        # Draw text
        cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)
        
    def _update_preview_widget(self, frame_tk):
        """Update preview widget in main thread"""
        if hasattr(self.parent_app, 'preview_label'):
            self.parent_app.preview_label.configure(image=frame_tk)
            self.parent_app.preview_label.image = frame_tk  # Keep reference

def main():
    root = tk.Tk()
    app = MultiTimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
