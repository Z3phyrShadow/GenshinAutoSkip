import time
import pyautogui
import cv2
import tkinter as tk
import threading
import keyboard

x1 = 240
y1 = 17
x2 = 345
y2 = 77

running = True

def is_image_on_screen(image_path, x1, y1, x2, y2):
    region = (x1, y1, x2 - x1, y2 - y1)
    try:
        location = pyautogui.locateOnScreen(image_path, region=region, confidence=0.8)
        return location is not None
    except Exception as e:
        print(f"Error: {e}")
        return False

def show_overlay(is_running):
    overlay = tk.Tk()
    overlay.overrideredirect(True)
    overlay.attributes("-topmost", True)
    overlay.attributes("-transparentcolor", "black")
    
    screen_width = overlay.winfo_screenwidth()
    overlay_width = 200
    overlay_height = 50
    x_position = (screen_width // 2) - (overlay_width // 2)
    overlay.geometry(f"{overlay_width}x{overlay_height}+{x_position}+10")
    overlay.config(bg="black")
    
    if is_running:
        text = "Auto Skipping"
        color = "green"
    else:
        text = "Not Auto Skipping"
        color = "red"

    label = tk.Label(
        overlay,
        text=text,
        fg=color,
        bg="black",
        font=("Arial", 10, "bold"),
    )
    label.pack(expand=True, fill="both")

    overlay.after(1000, overlay.destroy)
    overlay.mainloop()

def toggle_app():
    global running
    if running:
        print("App Disabled")
    else:
        print("App Enabled")
    running = not running 

def listen_for_hotkey():
    keyboard.add_hotkey('ctrl+shift+e', toggle_app)

threading.Thread(target=listen_for_hotkey, daemon=True).start()

image_path = "test.png"

while True:
    if is_image_on_screen(image_path, x1, y1, x2, y2):
        print("Image is visible on the screen.")

        if running:
            pyautogui.press("f")
            time.sleep(0.1)
            pyautogui.press("f")
        
        threading.Thread(target=show_overlay, args=(running,), daemon=True).start()
    else:
        print("Image is not visible on the screen.")
    
    time.sleep(0.5)
