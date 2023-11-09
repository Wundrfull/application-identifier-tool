import pygetwindow as gw
from overlay import Window as OverlayWindow
import tkinter as tk
from threading import Thread
import time

# This function creates a transparent overlay window with a yellow border
def create_overlay(target_window):
    root = tk.Tk()
    root.overrideredirect(True)  # Remove the window decorations
    root.geometry(f"{target_window.width}x{target_window.height}+{target_window.left}+{target_window.top}")
    root.lift()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", "white")

    # Create a canvas to draw the border
    canvas = tk.Canvas(root, highlightthickness=0, bg='white')
    canvas.pack(fill=tk.BOTH, expand=True)
    # Draw a yellow rectangle inside the canvas
    canvas.create_rectangle(
        10, 10, target_window.width-10, target_window.height-10,
        outline='yellow', width=4
    )
    
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
            current_state = (win.left, win.top, win.width, win.height, win.isMaximized, win.isActive)
            if current_state != last_state:
                print(f"Change detected in window: {title}")
                print(f"Location: ({win.left}, {win.top}), Size: {win.width}x{win.height}")
                print(f"Maximized: {win.isMaximized}, Active: {win.isActive}")
                # If a change is detected, create/update the overlay
                if last_state:
                    # Update the existing overlay
                    # You would add your update logic here
                    pass
                else:
                    # Create a new overlay
                    overlay_thread = Thread(target=create_overlay, args=(win,))
                    overlay_thread.daemon = True
                    overlay_thread.start()
                last_state = current_state
        else:
            print("Window not found. Exiting monitoring.")
            break
        time.sleep(1)

# Replace 'Your Window Title' with the actual title of the window you want to monitor
monitor_window('BakkesModInjectorCpp')
