import pygetwindow as gw
import tkinter as tk
from tkinter import ttk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Window Tracker")
        self.geometry("300x100")
        self.overlays = {}
        self.selected_window_title = tk.StringVar()
        self.currently_tracked_window = None

        # Dropdown for selecting the window to track
        self.dropdown = ttk.Combobox(self, textvariable=self.selected_window_title, width=50)
        self.dropdown.bind('<<ComboboxSelected>>', self.on_window_selection_change)
        self.update_dropdown()
        self.dropdown.pack(pady=5)

        # Button to refresh the list of windows
        self.refresh_button = ttk.Button(self, text="Refresh List", command=self.update_dropdown)
        self.refresh_button.pack(pady=5)

    def update_dropdown(self):
        """Update the dropdown list with the titles of all open windows, removing duplicates."""
        windows = list(set(gw.getAllTitles()))  # Set to remove duplicates, then back to list
        self.dropdown['values'] = sorted(windows)  # Sort for easier searching

    def on_window_selection_change(self, event=None):
        """Handle the event when a new window is selected from the dropdown."""
        selected_title = self.selected_window_title.get()

        # Cancel the update on the previously tracked window if any
        if self.currently_tracked_window:
            self.after_cancel(self.currently_tracked_window['update_id'])

        # Destroy the previous overlay if any
        if self.currently_tracked_window:
            overlay = self.currently_tracked_window['overlay']
            overlay.destroy()

        # Track the new window
        if selected_title:
            target_window = gw.getWindowsWithTitle(selected_title)[0]
            self.currently_tracked_window = {
                'title': selected_title,
                'overlay': self.create_overlay(target_window)
            }
            self.schedule_update(target_window)

    def create_overlay(self, target_window):
        # Create a new overlay window
        overlay = tk.Toplevel(self)
        overlay.overrideredirect(True)
        overlay.attributes('-topmost', 'true')
        overlay.geometry(f"{target_window.width}x{target_window.height}+{target_window.left}+{target_window.top}")
        canvas = tk.Canvas(overlay, highlightthickness=0, bg='white')
        canvas.pack(fill=tk.BOTH, expand=True)
        return canvas

    def schedule_update(self, target_window):
        # Update overlay window and canvas
        self.update_overlay(target_window)
        # Schedule the next update
        update_id = self.after(500, lambda: self.schedule_update(target_window))
        self.currently_tracked_window['update_id'] = update_id

    def update_overlay(self, target_window):
        # Find the target window again to get the updated position and size
        target_window = gw.getWindowsWithTitle(target_window.title)[0]
        overlay_canvas = self.currently_tracked_window['overlay']
        overlay_canvas.delete("all")

        # Update the geometry of the overlay window
        overlay_canvas.master.geometry(f"{target_window.width}x{target_window.height}+{target_window.left}+{target_window.top}")

        # Redraw the border and text
        overlay_canvas.create_rectangle(
            10, 10, target_window.width - 10, target_window.height - 10,
            outline='yellow', width=4, tag="border"
        )

        # Information text with black background rectangle
        info_text = f"Width: {target_window.width}, Height: {target_window.height}, X: {target_window.left}, Y: {target_window.top}"
        text_bg_width = overlay_canvas.winfo_width()
        text_bg_height = 20
        overlay_canvas.create_rectangle(
            target_window.width - text_bg_width, target_window.height - text_bg_height,
            target_window.width, target_window.height,
            fill="black", outline="black"
        )
        overlay_canvas.create_text(
            target_window.width - 5, target_window.height - 10,
            anchor='se', text=info_text,
            fill='white', font=('Helvetica', 9)
        )

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()
