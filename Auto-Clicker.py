# Hotkey Engineer Plugins Auto Clicker - A foundational plugin that provides customizable, automated mouse clicking functionality.
#
# Copyright (C) 2025 Eniti-Codes
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
import threading

pyautogui.PAUSE = 0

clicking_active = False
click_interval = 0.01
click_button = 'left'

click_thread = None

def perform_clicks():
    global clicking_active
    while clicking_active:
        if click_button == 'left':
            pyautogui.mouseDown(button='left')
            pyautogui.mouseUp(button='left')
        elif click_button == 'right':
            pyautogui.mouseDown(button='right')
            pyautogui.mouseUp(button='right')
        
        if click_interval > 0:
            time.sleep(click_interval)

def start_clicker():
    global clicking_active, click_thread
    if not clicking_active:
        try:
            new_interval = float(interval_entry.get())
            if new_interval < 0:
                messagebox.showwarning("Invalid Input", "Interval must be a non-negative number.")
                return
            
            global click_interval
            click_interval = new_interval
            
            global click_button
            click_button = button_var.get()

            clicking_active = True
            click_thread = threading.Thread(target=perform_clicks)
            click_thread.daemon = True
            click_thread.start()
            status_label.config(text=f"Status: Clicking {click_button.capitalize()} every {click_interval:.4f}s...")
            start_button.config(state=tk.DISABLED)
            stop_button.config(state=tk.NORMAL)
            interval_entry.config(state=tk.DISABLED)
            left_radio.config(state=tk.DISABLED)
            right_radio.config(state=tk.DISABLED)
            

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the interval.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not start clicker: {e}")
    else:
        status_label.config(text="Status: Already clicking!")

def stop_clicker():
    global clicking_active, click_thread
    if clicking_active:
        clicking_active = False
        status_label.config(text="Status: Stopped.")
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        interval_entry.config(state=tk.NORMAL)
        left_radio.config(state=tk.NORMAL)
        right_radio.config(state=tk.NORMAL)
    else:
        status_label.config(text="Status: Not active.")

root = tk.Tk()
root.title("Fast PyAuto Clicker")
root.geometry("400x300")
root.resizable(False, False)

interval_frame = ttk.LabelFrame(root, text="Click Interval")
interval_frame.pack(pady=10, padx=10, fill="x")

interval_label = ttk.Label(interval_frame, text="Interval (seconds):")
interval_label.pack(side="left", padx=5, pady=5)

interval_entry = ttk.Entry(interval_frame, width=15)
interval_entry.insert(0, str(click_interval))
interval_entry.pack(side="left", padx=5, pady=5)

button_frame = ttk.LabelFrame(root, text="Mouse Button")
button_frame.pack(pady=10, padx=10, fill="x")

button_var = tk.StringVar(value=click_button)

left_radio = ttk.Radiobutton(button_frame, text="Left Click", variable=button_var, value="left")
left_radio.pack(side="left", padx=20, pady=5)

right_radio = ttk.Radiobutton(button_frame, text="Right Click", variable=button_var, value="right")
right_radio.pack(side="right", padx=20, pady=5)

control_button_frame = ttk.Frame(root)
control_button_frame.pack(pady=10)

start_button = ttk.Button(control_button_frame, text="Start Clicking", command=start_clicker)
start_button.pack(side="left", padx=10)

stop_button = ttk.Button(control_button_frame, text="Stop Clicking", command=stop_clicker, state=tk.DISABLED)
stop_button.pack(side="right", padx=10)

status_label = ttk.Label(root, text="Status: Ready.", font=('Arial', 10))
status_label.pack(pady=10)

root.mainloop()
