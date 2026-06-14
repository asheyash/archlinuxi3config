import sys
import os
import atexit
import tkinter as tk
import subprocess

LOCK_FILE = "/tmp/my_volume_slider.lock"

def cleanup():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

atexit.register(cleanup)

def apply_volume_change(action):
    if action == "increase":
        subprocess.run(["pamixer", "-i", "5"])
    elif action == "decrease":
        subprocess.run(["pamixer", "-d", "5"])

# Determine action
action = "increase" if "--increase" in sys.argv else ("decrease" if "--decrease" in sys.argv else None)

# Handle already running instance
if os.path.exists(LOCK_FILE):
    if action: apply_volume_change(action)
    sys.exit()

# Handle initial launch
if action: apply_volume_change(action)
with open(LOCK_FILE, "w") as f: f.write("running")

# GUI Setup
root = tk.Tk()
root.title("Volume")
root.geometry("200x50")

def reset_timer(*args):
    if hasattr(root, 'timer_id'): root.after_cancel(root.timer_id)
    root.timer_id = root.after(4000, root.destroy)

def on_slider_change(val):
    subprocess.run(["pamixer", "--set-volume", str(int(float(val)))])
    reset_timer()

def sync_volume():
    actual_vol = int(subprocess.run(["pamixer", "--get-volume"], capture_output=True, text=True).stdout.strip())
    if abs(volume_bar.get() - actual_vol) > 1: volume_bar.set(actual_vol)
    root.after(100, sync_volume)

volume_bar = tk.Scale(root, from_=0, to=100, orient="horizontal", command=on_slider_change)
volume_bar.set(int(subprocess.run(["pamixer", "--get-volume"], capture_output=True, text=True).stdout.strip()))
volume_bar.pack()

sync_volume()
reset_timer()
root.mainloop()