import pygetwindow as gw
import tkinter as tk
from threading import Thread
import time

# A global dictionary to hold our overlays keyed by window titles
overlays = {}

# This function creates or updates a transparent overlay window with a yellow border
def create_or_update_overlay(target_window, title):
    # If the overlay already exists, update it
    if title in overlays:
        root = overlays[title]
        root.geometry(f"{target_window.width}x{target_window.height}+{target_window.left}+{target_window.top}")
        # You need to destroy the old canvas and create a new one to update the border
        for widget in root.winfo_children():
            widget.destroy()
        canvas = tk.Canvas(root, highlightthickness=0, bg='white')
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_rectangle(
            10, 10, target_window.width-10, target_window.height-10,
            outline='yellow', width=4
        )
    else:
        # Create a new overlay
        root = tk.Tk()
        root.overrideredirect(True)
        root.geometry(f"{target_window.width}x{target_window.height}+{target_window.left}+{target_window.top}")
        root.lift()
        root.wm_attributes("-topmost", True)
        root.wm_attributes("-transparentcolor", "white")
        canvas = tk.Canvas(root, highlightthickness=0, bg='white')
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_rectangle(
            10, 10, target_window.width-10, target_window.height-10,
            outline='yellow', width=4
        )
        overlays[title] = root
        
        # Function to keep the overlay window on top
        def keep_on_top(window):
            while True:
                window.lift()
                time.sleep(0.5)

        # Run the keep on top function in a separate thread
        top_thread = Thread(target=keep_on_top, args=(root,))
        top_thread.daemon = True
        top_thread.start()
        
        root.mainloop()

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
                overlays[title].destroy()
                del overlays[title]
            break
        time.sleep(1)

# Replace 'Your Window Title' with the actual title of the window you want to monitor
monitor_window('BakkesModInjectorCpp')
