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
