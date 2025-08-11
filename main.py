import tkinter as tk
from tkinter import ttk
import time
import threading

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
        self.root.title("Multi Timer")
        self.root.geometry("900x700")
        
        # Timer management
        self.timers = []
        self.max_timers = 10
        
        # Create GUI elements
        self.setup_ui()
        
        # Add the first timer
        self.add_timer()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Top controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=0, column=0, pady=(0, 5), sticky=(tk.W, tk.E))
        
        # Add timer button
        self.add_button = ttk.Button(controls_frame, text="+", command=self.add_timer, width=3)
        self.add_button.grid(row=0, column=0, padx=(0, 10))
        
        # Timer count label
        self.timer_count_label = ttk.Label(controls_frame, text="Timers: 1/10")
        self.timer_count_label.grid(row=0, column=1)
        
        # Create a canvas with scrollbar for timers
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.grid(row=1, column=0, pady=(0, 5), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.canvas = tk.Canvas(canvas_frame, height=400)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.timers_frame = ttk.Frame(self.canvas)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Create window in canvas for timers frame
        self.canvas_window = self.canvas.create_window((0, 0), window=self.timers_frame, anchor="nw")
        
        # Split history display (smaller, at bottom)
        history_frame = ttk.LabelFrame(main_frame, text="Split History", padding="3")
        history_frame.grid(row=2, column=0, pady=(5, 0), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create a compact scrollable text widget for split history
        self.split_history = tk.Text(history_frame, height=8, width=120, font=("Consolas", 8))
        history_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.split_history.yview)
        self.split_history.configure(yscrollcommand=history_scrollbar.set)
        
        self.split_history.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        history_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        
        # Bind canvas resize
        self.timers_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
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

def main():
    root = tk.Tk()
    app = MultiTimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
