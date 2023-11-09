import pygetwindow as gw
import tkinter as tk
import time

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overlays = {}
        self.overrideredirect(True)  # Remove window decorations
        self.attributes('-alpha', 0)  # Make the root window invisible

    def create_or_update_overlay(self, target_window, title):
        if title in self.overlays:
            # Update existing overlay
            overlay, canvas = self.overlays[title]
            overlay.geometry(f"{target_window.width}x{target_window.height}+{target_window.left}+{target_window.top}")
            canvas.delete("all")  # Delete the old border and text
            # Draw a new border
            canvas.create_rectangle(
                10, 10, target_window.width - 10, target_window.height - 10,
                outline='yellow', width=4, tag="border"
            )
            # Display the window info in red color with opaque background
            window_info = f"Width: {target_window.width}, Height: {target_window.height}, X: {target_window.left}, Y: {target_window.top}"
            text_position = (target_window.width - 10, target_window.height - 10)
            canvas.create_rectangle(
                text_position[0] - 200, text_position[1] - 15,  # 200 is an estimated width of the text background, adjust as needed
                text_position[0], text_position[1],
                fill="white", outline="white", tag="info_bg"
            )
            canvas.create_text(
                text_position, anchor="se", text=window_info,
                fill="red", font=("Helvetica", 10), tag="info"
            )
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
            canvas.create_rectangle(
                10, 10, target_window.width - 10, target_window.height - 10,
                outline='yellow', width=4, tag="border"
            )
            # Display the window info in red color with opaque background
            window_info = f"Width: {target_window.width}, Height: {target_window.height}, X: {target_window.left}, Y: {target_window.top}"
            text_position = (target_window.width - 10, target_window.height - 10)
            canvas.create_rectangle(
                text_position[0] - 200, text_position[1] - 15,  # 200 is an estimated width of the text background, adjust as needed
                text_position[0], text_position[1],
                fill="white", outline="white", tag="info_bg"
            )
            canvas.create_text(
                text_position, anchor="se", text=window_info,
                fill="red", font=("Helvetica", 10), tag="info"
            )
            self.overlays[title] = (overlay, canvas)

    def monitor_window(self, title):
        win = gw.getWindowsWithTitle(title)
        if win:
            win = win[0]
            self.create_or_update_overlay(win, title)
        else:
            if title in self.overlays:
                overlay, _ = self.overlays[title]
                overlay.destroy()
                del self.overlays[title]

        # Schedule the next check
        self.after(1000, self.monitor_window, title)

if __name__ == "__main__":
    app = Application()
    # Replace 'Your Window Title' with the actual title of the window you want to monitor
    app.after(1000, app.monitor_window, 'BakkesModInjectorCpp')
    app.mainloop()
