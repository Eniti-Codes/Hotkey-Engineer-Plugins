# Hotkey Engineer Plugins Key Prasser - A utility designed to rapidly and repeatedly press a single key that you've configured it for.
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

# pyautogui.PAUSE = 0  # Not strictly necessary for key presses, but good to keep if you might add mouse movements later

key_pressing_active = False
press_interval = 0.1 # Default interval for key presses
key_to_press = 'space' # Default key to press (e.g., for jump)

press_thread = None

def perform_key_presses():
    global key_pressing_active
    while key_pressing_active:
        pyautogui.press(key_to_press)
        
        if press_interval > 0:
            time.sleep(press_interval)

def start_key_presser():
    global key_pressing_active, press_thread
    if not key_pressing_active:
        try:
            new_interval = float(interval_entry.get())
            if new_interval < 0:
                messagebox.showwarning("Invalid Input", "Interval must be a non-negative number.")
                return
            
            global press_interval
            press_interval = new_interval
            
            global key_to_press
            entered_key = key_entry.get().strip()
            if not entered_key:
                messagebox.showwarning("Invalid Input", "Please enter a key to press.")
                return
            key_to_press = entered_key.lower() # Store in lowercase for consistency

            key_pressing_active = True
            press_thread = threading.Thread(target=perform_key_presses)
            press_thread.daemon = True
            press_thread.start()
            status_label.config(text=f"Status: Pressing '{key_to_press}' every {press_interval:.4f}s...")
            start_button.config(state=tk.DISABLED)
            stop_button.config(state=tk.NORMAL)
            interval_entry.config(state=tk.DISABLED)
            key_entry.config(state=tk.DISABLED)
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the interval.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not start key presser: {e}")
    else:
        status_label.config(text="Status: Already pressing keys!")

def stop_key_presser():
    global key_pressing_active, press_thread
    if key_pressing_active:
        key_pressing_active = False
        status_label.config(text="Status: Stopped.")
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        interval_entry.config(state=tk.NORMAL)
        key_entry.config(state=tk.NORMAL)
    else:
        status_label.config(text="Status: Not active.")

# --- GUI Setup ---
root = tk.Tk()
root.title("Auto Key Presser")
root.geometry("400x300")
root.resizable(False, False)

# Interval Frame
interval_frame = ttk.LabelFrame(root, text="Press Interval")
interval_frame.pack(pady=10, padx=10, fill="x")

interval_label = ttk.Label(interval_frame, text="Interval (seconds):")
interval_label.pack(side="left", padx=5, pady=5)

interval_entry = ttk.Entry(interval_frame, width=15)
interval_entry.insert(0, str(press_interval))
interval_entry.pack(side="left", padx=5, pady=5)

# Key Selection Frame
key_frame = ttk.LabelFrame(root, text="Key to Press")
key_frame.pack(pady=10, padx=10, fill="x")

key_label = ttk.Label(key_frame, text="Key (e.g., 'space', 'w', 'enter'):")
key_label.pack(side="left", padx=5, pady=5)

key_entry = ttk.Entry(key_frame, width=15)
key_entry.insert(0, key_to_press) # Set default key
key_entry.pack(side="left", padx=5, pady=5)

# Control Buttons Frame
control_button_frame = ttk.Frame(root)
control_button_frame.pack(pady=10)

start_button = ttk.Button(control_button_frame, text="Start Pressing", command=start_key_presser)
start_button.pack(side="left", padx=10)

stop_button = ttk.Button(control_button_frame, text="Stop Pressing", command=stop_key_presser, state=tk.DISABLED)
stop_button.pack(side="right", padx=10)

# Status Label
status_label = ttk.Label(root, text="Status: Ready.", font=('Arial', 10))
status_label.pack(pady=10)

root.mainloop()
