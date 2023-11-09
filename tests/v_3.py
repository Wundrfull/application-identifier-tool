import pygetwindow as gw
import tkinter as tk
from threading import Thread
import time

# A dictionary to hold our overlays keyed by window titles
overlays = {}

# This function creates or updates a transparent overlay window with a yellow border
def create_or_update_overlay(target_window, title):
    if title in overlays:
        # Update existing overlay
        overlay, canvas = overlays[title]
        overlay.geometry(f"{target_window.width}x{target_window.height}+{target_window.left}+{target_window.top}")
        canvas.delete("border")  # Delete the old border
        # Draw a new border
        canvas.create_rectangle(
            10, 10, target_window.width-10, target_window.height-10,
            outline='yellow', width=4, tag="border"
        )
    else:
        # Create a new overlay
        overlay = tk.Tk()
        overlay.overrideredirect(True)  # Remove window decorations
        overlay.geometry(f"{target_window.width}x{target_window.height}+{target_window.left}+{target_window.top}")
        overlay.lift()
        overlay.wm_attributes("-topmost", True)
        overlay.wm_attributes("-transparentcolor", "white")

        canvas = tk.Canvas(overlay, highlightthickness=0, bg='white')
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_rectangle(
            10, 10, target_window.width-10, target_window.height-10,
            outline='yellow', width=4, tag="border"
        )
        overlays[title] = (overlay, canvas)
        
        # Start the Tkinter event loop in a separate thread
        Thread(target=lambda: overlay.mainloop(), daemon=True).start()

def update_overlay():
    while True:
        for title, (overlay, canvas) in overlays.items():
            win = gw.getWindowsWithTitle(title)
            if win:
                win = win[0]
                overlay.geometry(f"{win.width}x{win.height}+{win.left}+{win.top}")
                canvas.delete("border")
                canvas.create_rectangle(
                    10, 10, win.width-10, win.height-10,
                    outline='yellow', width=4, tag="border"
                )
            else:
                # If the window is not found, destroy the overlay
                overlay.destroy()
                del overlays[title]
        time.sleep(1)

# Function to monitor a specific window for changes
def monitor_window(title):
    print(f"Monitoring the window: {title}")
    last_state = None
    while True:
        win = gw.getWindowsWithTitle(title)
        if win:
            win = win[0]
            current_state = (win.left, win.top, win.width, win.height)
            if current_state != last_state:
                print(f"Change detected in window: {title}")
                print(f"Location: ({win.left}, {win.top}), Size: {win.width}x{win.height}")
                create_or_update_overlay(win, title)
                last_state = current_state
        else:
            print(f"Window {title} has been closed.")
            if title in overlays:
                overlays[title][0].destroy()
                del overlays[title]
            break
        time.sleep(1)

# Start the monitoring in a separate thread
Thread(target=lambda: monitor_window('BakkesModInjectorCpp'), daemon=True).start()

# Start the overlay update loop
update_overlay()
