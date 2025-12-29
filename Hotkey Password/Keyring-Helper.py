# Hotkey Engineer Plugins Keyring Helper - Integrates with your system's keyring to securely type passwords into a password manager.
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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ----- > Configure this <-----
VENV_FOLDER_NAME = "venv"

VENV_PYTHON_EXEC = os.path.join(SCRIPT_DIR, VENV_FOLDER_NAME, 'bin', 'python3')

# ----- > Configure this <-----
MAIN_SCRIPT = os.path.join(SCRIPT_DIR, 'Keyring.py')

if not os.path.exists(VENV_PYTHON_EXEC):
    print(f"ERROR: Virtual environment Python executable not found at: {VENV_PYTHON_EXEC}")
    print(f"Please ensure '{VENV_FOLDER_NAME}' is correct and the venv is created and installed.")
    sys.exit(1)

command = [VENV_PYTHON_EXEC, MAIN_SCRIPT] + sys.argv[1:]

print(f"DEBUG Launcher: Executing command: {' '.join(command)}")

result = subprocess.run(command, check=False, env=os.environ)

sys.exit(result.returncode)
