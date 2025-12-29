# Hotkey Engineer Plugins Bash_runer.py - This allows hockey engineer to run bash script.
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

import subprocess
import os
import sys

# =================================================================
BASH_SCRIPT_PATH = '/home/you/Bash_script.sh'
# =================================================================

def run_in_new_terminal():
    """
    Attempts to open a new terminal window to execute the bash script,
    prioritizing 'terminator' for Linux Mint.
    """
    
    script_to_run = BASH_SCRIPT_PATH
    
    print("--- Running script in a new terminal window ---")

    if not os.path.exists(script_to_run):
        print(f"Error: Bash script not found at the specified path: {script_to_run}")
        return

    terminals = ['terminator', 'gnome-terminal', 'xterm']

    for terminal in terminals:
        try:
            print(f"Attempting to launch script using '{terminal}'...")
            
            command = f'bash -c "{script_to_run}; exec bash"'
            
            if terminal == 'terminator':
                subprocess.Popen([terminal, '-e', command])
            elif terminal == 'gnome-terminal':
                subprocess.Popen([terminal, '--', 'bash', '-c', command])
            elif terminal == 'xterm':
                subprocess.Popen([terminal, '-e', command])
            
            print(f"Successfully launched '{script_to_run}' in a new '{terminal}' window.")
            return

        except FileNotFoundError:
            print(f"'{terminal}' was not found. Trying the next option...")
        except Exception as e:
            print(f"An unexpected error occurred while trying to launch '{terminal}': {e}")
            
    print("\nNo supported terminal application was found. Please install one or modify the script.")

if __name__ == "__main__":
    if os.path.exists(BASH_SCRIPT_PATH):
        os.chmod(BASH_SCRIPT_PATH, 0o755)
    
    run_in_new_terminal()
