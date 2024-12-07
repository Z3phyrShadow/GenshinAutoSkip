import tkinter as tk
import threading
import keyboard
import pyautogui
import cv2
import numpy as np
import os
import sys
import time

x1, y1, x2, y2 = 240, 17, 345, 77
running = True
found_location = None

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

image_path = os.path.join(base_path, "test.png")
template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]

def find_image():
    global found_location
    while True:
        if not running:
            time.sleep(0.5)
            continue

        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > 0.8:
            found_location = (max_loc[0] + x1, max_loc[1] + y1, w, h)
            pyautogui.press("f")
        else:
            found_location = None

        time.sleep(0.1)

def toggle_app():
    global running
    running = not running
    print("App Enabled" if running else "App Disabled")

def quit_app():
    os._exit(0)

def update_text_overlay(status_label):
    status_label.config(
        text="Auto Skipping" if running else "Not Auto Skipping",
        fg="green" if running else "red",
    )

def update_box_overlay(canvas):
    canvas.delete("all")
    if found_location and running:
        x, y, w, h = found_location
        canvas.create_rectangle(
            x - x1, y - y1, x - x1 + w, y - y1 + h, outline="red", width=2
        )

def main():
    global found_location

    keyboard.add_hotkey("ctrl+shift+e", toggle_app)
    keyboard.add_hotkey("ctrl+shift+q", quit_app)

    screen_width = pyautogui.size().width

    # Create text overlay
    text_root = tk.Tk()
    text_root.overrideredirect(True)
    text_root.attributes("-topmost", True)
    text_root.attributes("-transparentcolor", "black")
    text_width = 300
    text_root.geometry(f"{text_width}x50+{(screen_width - text_width) // 2}+10")
    text_root.config(bg="black")
    status_label = tk.Label(
        text_root, text="Not Auto Skipping", fg="red", bg="black", font=("Arial", 12, "bold")
    )
    status_label.pack()

    # Create box overlay
    box_root = tk.Tk()
    box_root.overrideredirect(True)
    box_root.attributes("-topmost", True)
    box_root.attributes("-transparentcolor", "black")
    box_root.geometry(f"{x2 - x1}x{y2 - y1}+{x1}+{y1}")
    box_root.config(bg="black")
    canvas = tk.Canvas(box_root, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    def periodic_update():
        update_text_overlay(status_label)
        update_box_overlay(canvas)
        text_root.after(100, periodic_update)

    threading.Thread(target=find_image, daemon=True).start()

    periodic_update()
    text_root.mainloop()

if __name__ == "__main__":
    main()
