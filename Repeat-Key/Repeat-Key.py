# Hotkey Engineer Plugins Repeat-Key - is a high-performance, modern automation utility for mouse and keyboard tasks. Featuring a clean UI and millisecond precision, it is designed to work as a standalone tool or as a seamless plugin for Hotkey Engineer.
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
import json
import os
import sv_ttk

# Optimization and Safety
pyautogui.PAUSE = 0 
pyautogui.FAILSAFE = True
SETTINGS_FILE = 'settings.json'

clicking_active = False
key_pressing_active = False
click_thread = None
press_thread = None

# Default settings (used if no file exists)
default_settings = {
    'click_interval': 0.01,
    'click_button': 'left',
    'press_interval': 0.1,
    'key_to_press': 'space',
    'theme_mode': 'light'
}
current_settings = default_settings.copy()
current_theme_mode = current_settings['theme_mode']

# Global References for UI Widgets
clicker_interval_entry_ref = None
clicker_button_var_ref = None
presser_interval_entry_ref = None
key_entry_ref = None
clicker_start_button_ref = None
clicker_stop_button_ref = None
presser_start_button_ref = None
presser_stop_button_ref = None
notebook_ref = None
clicker_status_label_ref = None
presser_status_label_ref = None
clicker_left_radio_ref = None
clicker_right_radio_ref = None

# --- Settings Management Functions ---
def load_settings():
    """Loads settings from the JSON file."""
    global current_settings, current_theme_mode
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                loaded_settings = json.load(f)
                for key, default_value in default_settings.items():
                    current_settings[key] = loaded_settings.get(key, default_value)
                current_theme_mode = current_settings['theme_mode']
        except Exception as e:
            print(f"Error loading settings: {e}. Using defaults.")
    
def save_settings():
    """Gathers current settings from globally referenced widgets and saves them."""
    global current_settings, current_theme_mode
    
    if clicker_interval_entry_ref is None:
        return

    try:
        current_settings['click_interval'] = float(clicker_interval_entry_ref.get())
    except ValueError: pass
        
    current_settings['click_button'] = clicker_button_var_ref.get()
    
    try:
        current_settings['press_interval'] = float(presser_interval_entry_ref.get())
    except ValueError: pass
        
    current_settings['key_to_press'] = key_entry_ref.get().strip().lower()
    current_settings['theme_mode'] = current_theme_mode
    
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(current_settings, f, indent=4)
    except Exception as e:
        print(f"ERROR: Could not save settings: {e}")

def on_closing():
    """Handler for closing the window. Stops threads and destroys root."""
    global clicking_active, key_pressing_active
    clicking_active = False
    key_pressing_active = False
    time.sleep(0.05) 
    root.destroy()

# --- Theme Management ---
def toggle_dark_mode():
    """Switches the theme between Light/Dark mode and saves it."""
    global current_theme_mode
    if current_theme_mode == "light":
        sv_ttk.set_theme("dark")
        current_theme_mode = "dark"
    else:
        sv_ttk.set_theme("light")
        current_theme_mode = "light"
    save_settings()

# --- Universal Toggle Fix ---
def f6_toggle_active(event=None):
    """
    Checks the currently active process and toggles it. 
    If neither is active, it starts the function on the currently visible tab.
    """
    global clicking_active, key_pressing_active

    # If something is running, STOP IT
    if clicking_active:
        stop_clicker(clicker_status_label_ref, clicker_start_button_ref, clicker_stop_button_ref, clicker_interval_entry_ref, clicker_left_radio_ref, clicker_right_radio_ref)
    elif key_pressing_active:
        stop_key_presser(presser_status_label_ref, presser_start_button_ref, presser_stop_button_ref, presser_interval_entry_ref, key_entry_ref)
    
    else:
        current_tab_id = notebook_ref.select()
        current_tab_index = notebook_ref.index(current_tab_id)

        if current_tab_index == 0:
            start_clicker(clicker_interval_entry_ref, clicker_button_var_ref, clicker_status_label_ref, clicker_start_button_ref, clicker_stop_button_ref, root)
        elif current_tab_index == 1:
            start_key_presser(presser_interval_entry_ref, key_entry_ref, presser_status_label_ref, presser_start_button_ref, presser_stop_button_ref, root)

# --- Auto Clicker Logic ---
def perform_clicks(interval, button):
    global clicking_active
    while clicking_active:
        pyautogui.click(button=button)
        if interval > 0:
            time.sleep(interval)

def start_clicker(interval_entry, button_var, status_label, start_button, stop_button, root_window):
    global clicking_active, click_thread, click_interval, click_button
    
    if clicking_active: return
    
    try:
        new_interval = float(interval_entry.get())
        if new_interval < 0:
            messagebox.showwarning("Invalid Input", "Interval must be non-negative.", parent=root_window)
            return

        click_interval = new_interval
        click_button = button_var.get()
        clicking_active = True
        
        click_thread = threading.Thread(target=perform_clicks, args=(click_interval, click_button))
        click_thread.daemon = True
        click_thread.start()
        
        status_label.config(text=f"Status: Clicking {click_button.capitalize()} at {click_interval:.4f}s.")
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        interval_entry.config(state=tk.DISABLED)
        clicker_left_radio_ref.config(state=tk.DISABLED)
        clicker_right_radio_ref.config(state=tk.DISABLED)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the interval.", parent=root_window)

def stop_clicker(status_label, start_button, stop_button, interval_entry, left_radio, right_radio):
    global clicking_active
    if clicking_active:
        clicking_active = False
        save_settings() 
        status_label.config(text="Status: Idle.")
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        interval_entry.config(state=tk.NORMAL)
        left_radio.config(state=tk.NORMAL)
        right_radio.config(state=tk.NORMAL)

# --- Key Presser Logic ---
def perform_key_presses(interval, key):
    global key_pressing_active
    while key_pressing_active:
        pyautogui.press(key)
        if interval > 0:
            time.sleep(interval)

def start_key_presser(interval_entry, key_entry, status_label, start_button, stop_button, root_window):
    global key_pressing_active, press_thread, press_interval, key_to_press

    if key_pressing_active: return

    try:
        new_interval = float(interval_entry.get())
        if new_interval < 0:
            messagebox.showwarning("Invalid Input", "Interval must be non-negative.", parent=root_window)
            return

        entered_key = key_entry.get().strip().lower()
        
        # --- BLACKLIST FIX ---
        if entered_key == 'f6':
            messagebox.showwarning("Reserved Key", "F6 is the Start/Stop toggle. Please choose a different key.", parent=root_window)
            return

        if not entered_key:
            messagebox.showwarning("Invalid Input", "Please enter a key to press.", parent=root_window)
            return

        press_interval = new_interval
        key_to_press = entered_key
        key_pressing_active = True
        
        press_thread = threading.Thread(target=perform_key_presses, args=(press_interval, key_to_press))
        press_thread.daemon = True
        press_thread.start()

        status_label.config(text=f"Status: Pressing '{key_to_press}' at {press_interval:.4f}s.")
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        interval_entry.config(state=tk.DISABLED)
        key_entry.config(state=tk.DISABLED)
        
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the interval.", parent=root_window)

def stop_key_presser(status_label, start_button, stop_button, interval_entry, key_entry):
    global key_pressing_active
    if key_pressing_active:
        key_pressing_active = False
        save_settings() 
        status_label.config(text="Status: Idle.")
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        interval_entry.config(state=tk.NORMAL)
        key_entry.config(state=tk.NORMAL)

# --- Main Application Setup ---
load_settings()

root = tk.Tk() 
root.title("Repeat Key!")
root.geometry("450x380")
root.resizable(False, False)

sv_ttk.set_theme(current_theme_mode) 

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

options_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Toggle Theme (Dark/Light)", command=toggle_dark_mode)
options_menu.add_separator()
options_menu.add_command(label="Exit", command=on_closing)

# Binding F6
root.bind_all('<F6>', f6_toggle_active)

notebook = ttk.Notebook(root)
notebook.pack(pady=10, padx=10, expand=True, fill="both")
notebook_ref = notebook 

# --- Clicker UI ---
clicker_frame = ttk.Frame(notebook, padding="10")
notebook.add(clicker_frame, text='Auto Clicker') 

clicker_interval_frame = ttk.LabelFrame(clicker_frame, text="Click Frequency")
clicker_interval_frame.pack(pady=10, padx=10, fill="x")
ttk.Label(clicker_interval_frame, text="Interval (seconds):").pack(side="left", padx=5, pady=5)
clicker_interval_entry = ttk.Entry(clicker_interval_frame, width=15)
clicker_interval_entry.insert(0, str(current_settings['click_interval']))
clicker_interval_entry.pack(side="left", padx=5, pady=5)
clicker_interval_entry_ref = clicker_interval_entry

clicker_button_frame = ttk.LabelFrame(clicker_frame, text="Mouse Button Selection")
clicker_button_frame.pack(pady=10, padx=10, fill="x")
clicker_button_var = tk.StringVar(value=current_settings['click_button'])
clicker_button_var_ref = clicker_button_var
clicker_left_radio = ttk.Radiobutton(clicker_button_frame, text="Left Button", variable=clicker_button_var, value="left")
clicker_left_radio.pack(side="left", padx=20, pady=5)
clicker_right_radio = ttk.Radiobutton(clicker_button_frame, text="Right Button", variable=clicker_button_var, value="right")
clicker_right_radio.pack(side="right", padx=20, pady=5)
clicker_left_radio_ref = clicker_left_radio
clicker_right_radio_ref = clicker_right_radio

clicker_control_button_frame = ttk.Frame(clicker_frame)
clicker_control_button_frame.pack(pady=20)

clicker_start_button = ttk.Button(clicker_control_button_frame, text="Start", command=lambda: start_clicker(clicker_interval_entry, clicker_button_var, clicker_status_label_ref, clicker_start_button, clicker_stop_button, root))
clicker_start_button.pack(side="left", padx=10)
clicker_stop_button = ttk.Button(clicker_control_button_frame, text="Stop", command=lambda: stop_clicker(clicker_status_label_ref, clicker_start_button, clicker_stop_button, clicker_interval_entry, clicker_left_radio, clicker_right_radio), state=tk.DISABLED)
clicker_stop_button.pack(side="right", padx=10)
clicker_start_button_ref = clicker_start_button
clicker_stop_button_ref = clicker_stop_button

clicker_status_label = ttk.Label(clicker_frame, text="Status: Idle.", font=('Arial', 10))
clicker_status_label.pack(pady=10)
clicker_status_label_ref = clicker_status_label

# --- Key Presser UI ---
key_presser_frame = ttk.Frame(notebook, padding="10")
notebook.add(key_presser_frame, text='Auto Key Presser')

presser_interval_frame = ttk.LabelFrame(key_presser_frame, text="Key Press Frequency")
presser_interval_frame.pack(pady=10, padx=10, fill="x")
ttk.Label(presser_interval_frame, text="Interval (seconds):").pack(side="left", padx=5, pady=5)
presser_interval_entry = ttk.Entry(presser_interval_frame, width=15)
presser_interval_entry.insert(0, str(current_settings['press_interval']))
presser_interval_entry.pack(side="left", padx=5, pady=5)
presser_interval_entry_ref = presser_interval_entry

key_frame = ttk.LabelFrame(key_presser_frame, text="Key Selection")
key_frame.pack(pady=10, padx=10, fill="x")
ttk.Label(key_frame, text="Key to press (e.g., 'space', 'w', 'enter'):").pack(side="left", padx=5, pady=5)
key_entry = ttk.Entry(key_frame, width=15)
key_entry.insert(0, current_settings['key_to_press'])
key_entry.pack(side="left", padx=5, pady=5)
key_entry_ref = key_entry

presser_control_button_frame = ttk.Frame(key_presser_frame)
presser_control_button_frame.pack(pady=20)

presser_start_button = ttk.Button(presser_control_button_frame, text="Start", command=lambda: start_key_presser(presser_interval_entry, key_entry, presser_status_label_ref, presser_start_button, presser_stop_button, root))
presser_start_button.pack(side="left", padx=10)
presser_stop_button = ttk.Button(presser_control_button_frame, text="Stop", command=lambda: stop_key_presser(presser_status_label_ref, presser_start_button, presser_stop_button, presser_interval_entry, key_entry), state=tk.DISABLED)
presser_stop_button.pack(side="right", padx=10)
presser_start_button_ref = presser_start_button
presser_stop_button_ref = presser_stop_button

presser_status_label = ttk.Label(key_presser_frame, text="Status: Idle.", font=('Arial', 10))
presser_status_label.pack(pady=10)
presser_status_label_ref = presser_status_label

ttk.Label(root, text="F6: Universal Start/Stop Toggle", font=('Arial', 8, 'bold')).pack(pady=5)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()