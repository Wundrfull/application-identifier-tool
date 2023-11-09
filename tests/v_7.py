import pygetwindow as gw
import tkinter as tk
from tkinter import ttk
import time
from threading import Thread

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Window Tracker")
        self.geometry("300x100")
        self.overlays = {}
        self.selected_window_title = tk.StringVar()

        # Dropdown for selecting the window to track
        self.dropdown = ttk.Combobox(self, textvariable=self.selected_window_title, width=50)
        self.dropdown.bind('<<ComboboxSelected>>', self.on_window_selection_change)
        self.update_dropdown()
        self.dropdown.pack(pady=5)

        # Button to refresh the list of windows
        self.refresh_button = ttk.Button(self, text="Refresh List", command=self.update_dropdown)
        self.refresh_button.pack(pady=5)

    def update_dropdown(self):
        """Update the dropdown list with the titles of all open windows."""
        windows = gw.getAllTitles()
        current_value = self.dropdown.get()
        self.dropdown['values'] = windows
        if current_value in windows:
            self.dropdown.set(current_value)
        elif windows:
            self.dropdown.set(windows[0])
        else:
            self.dropdown.set('')

    def on_window_selection_change(self, event=None):
        """Handle the event when a new window is selected from the dropdown."""
        title = self.selected_window_title.get()
        if title:
            self.create_or_update_overlay(title)

    def create_or_update_overlay(self, title):
        target_window = gw.getWindowsWithTitle(title)[0]
        if title in self.overlays:
            # Update existing overlay
            overlay, canvas = self.overlays[title]
            overlay.geometry(f"{target_window.width}x{target_window.height}+{target_window.left}+{target_window.top}")
            canvas.delete("all")  # Delete the old border and text
        else:
            # Create a new overlay
            overlay = tk.Toplevel(self)
            overlay.overrideredirect(True)
            overlay.geometry(f"{target_window.width}x{target_window.height}+{target_window.left}+{target_window.top}")
            overlay.lift()
            overlay.wm_attributes("-topmost", True)
            overlay.wm_attributes("-transparentcolor", "white")

            canvas = tk.Canvas(overlay, highlightthickness=0, bg='white')
            canvas.pack(fill=tk.BOTH, expand=True)
            self.overlays[title] = (overlay, canvas)
        
        # Draw the border and text
        canvas.create_rectangle(
            10, 10, target_window.width - 10, target_window.height - 10,
            outline='yellow', width=4, tag="border"
        )
        window_info = f"Width: {target_window.width}, Height: {target_window.height}, X: {target_window.left}, Y: {target_window.top}"
        text_position = (target_window.width - 10, target_window.height - 10)
        canvas.create_rectangle(
            text_position[0] - 210, text_position[1] - 20,
            text_position[0], text_position[1],
            fill="white", outline="white", tag="info_bg"
        )
        canvas.create_text(
            text_position, anchor="se", text=window_info,
            fill="black", font=("Helvetica", 9), tag="info"
        )

        # Schedule updates
        self.after(1000, lambda: self.update_overlay(title))

    def update_overlay(self, title):
        # If the window is closed, remove its overlay
        if title not in gw.getAllTitles():
            overlay, _ = self.overlays.pop(title, (None, None))
            if overlay:
                overlay.destroy()
            return

        # If the window exists, update the overlay
        target_window = gw.getWindowsWithTitle(title)[0]
        overlay, canvas = self.overlays.get(title, (None, None))
        if overlay and canvas:
            overlay.geometry(f"{target_window.width}x{target_window.height}+{target_window.left}+{target_window.top}")
            canvas.coords("border", 10, 10, target_window.width - 10, target_window.height - 10)
            window_info = f"Width: {target_window.width}, Height: {target_window.height}, X: {target_window.left}, Y: {target_window.top}"
            text_position = (target_window.width - 10, target_window.height - 10)
            canvas.coords("info_bg", text_position[0] - 210, text_position[1] - 20, text_position[0], text_position[1])
            canvas.itemconfig("info", text=window_info)
            canvas.coords("info", text_position)
            self.after(1000, lambda: self.update_overlay(title))

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()
