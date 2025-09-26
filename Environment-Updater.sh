#!/bin/bash

# Hotkey Engineer Plugins Environment Updater - Modify '$SERVICE_FILE' to include environment variables in ExecStart
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

# --- Configuration ---
SERVICE_NAME="hotkey-engineer.service"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}"
# IMPORTANT: This MUST EXACTLY match the command part of your ExecStart line.
# Based on your input, it is:
ORIGINAL_PYTHON_COMMAND="/opt/hotkey_engineer/venv/bin/python3 /opt/hotkey_engineer/venv/Hotkey-Engineer.py"
# --- End Configuration ---

echo "--- Hotkey Engineer Environment Updater ---"
echo "Updating environment variables for systemd service: '$SERVICE_NAME'"
echo "Service file: '$SERVICE_FILE'"
echo ""

# Check if SERVICE_FILE exists
if [ ! -f "$SERVICE_FILE" ]; then
    echo "ERROR: Systemd service file '$SERVICE_FILE' not found."
    echo "Please ensure Hotkey Engineer is correctly installed as a systemd service."
    exit 1
fi

echo "1. Detecting current user's session environment variables..."

CURRENT_DISPLAY=$(printenv DISPLAY)
if [ -z "$CURRENT_DISPLAY" ]; then
    echo "  WARNING: DISPLAY environment variable not found. Defaulting to :0."
    CURRENT_DISPLAY=":0"
else
    echo "  Detected DISPLAY: $CURRENT_DISPLAY"
fi

CURRENT_DBUS_ADDRESS=$(printenv DBUS_SESSION_BUS_ADDRESS)
if [ -z "$CURRENT_DBUS_ADDRESS" ]; then
    echo "  ERROR: Could not detect DBUS_SESSION_BUS_ADDRESS. Keyring access may fail."
    echo "  Please ensure you are running this script from a graphical terminal *after* logging in."
    exit 1
else
    echo "  Detected DBUS_SESSION_BUS_ADDRESS: $CURRENT_DBUS_ADDRESS"
fi

CURRENT_XDG_RUNTIME_DIR=$(printenv XDG_RUNTIME_DIR)
if [ -z "$CURRENT_XDG_RUNTIME_DIR" ]; then
    echo "  ERROR: Could not detect XDG_RUNTIME_DIR. Keyring access may fail."
    echo "  Please ensure you are running this script from a graphical terminal *after* logging in."
    exit 1
else
    echo "  Detected XDG_RUNTIME_DIR: $CURRENT_XDG_RUNTIME_DIR"
fi

echo ""

echo "2. Modifying '$SERVICE_FILE' to include environment variables in ExecStart..."

# Escape values for sed for proper inclusion in the command string
ESCAPED_DISPLAY=$(printf '%s\n' "$CURRENT_DISPLAY" | sed -e 's/[]\/$*.^[]/\\&/g')
ESCAPED_DBUS_ADDRESS=$(printf '%s\n' "$CURRENT_DBUS_ADDRESS" | sed -e 's/[]\/$*.^[]/\\&/g')
ESCAPED_XDG_RUNTIME_DIR=$(printf '%s\n' "$CURRENT_XDG_RUNTIME_DIR" | sed -e 's/[]\/$*.^[]/\\&/g')
ESCAPED_ORIGINAL_PYTHON_COMMAND=$(printf '%s\n' "$ORIGINAL_PYTHON_COMMAND" | sed -e 's/[]\/$*.^[]/\\&/g')

# Construct the new ExecStart line that includes exports
NEW_EXEC_START_COMMAND_RAW="/bin/bash -lc \"export DISPLAY='${ESCAPED_DISPLAY}'; export DBUS_SESSION_BUS_ADDRESS='${ESCAPED_DBUS_ADDRESS}'; export XDG_RUNTIME_DIR='${ESCAPED_XDG_RUNTIME_DIR}'; exec ${ESCAPED_ORIGINAL_PYTHON_COMMAND}\""

# Escape the entire new command for the sed 's' command
ESCAPED_SED_NEW_EXEC_START_COMMAND=$(printf '%s\n' "$NEW_EXEC_START_COMMAND_RAW" | sed -e 's/[]\/$*.^[]/\\&/g')

# Update the ExecStart line in the service file
if grep -q "^ExecStart=" "$SERVICE_FILE"; then
    sudo sed -i "s|^ExecStart=.*|ExecStart=${NEW_EXEC_START_COMMAND_RAW}|" "$SERVICE_FILE"
    echo "  - Updated ExecStart line."
else
    echo "  WARNING: ExecStart line not found. Cannot modify service file."
    echo "  Please add 'ExecStart=${NEW_EXEC_START_COMMAND_RAW}' manually to '$SERVICE_FILE'."
    exit 1
fi

# Optional: Remove EnvironmentFile line if it exists to avoid redundancy or confusion
if grep -q "^EnvironmentFile=" "$SERVICE_FILE"; then
    sudo sed -i "/^EnvironmentFile=/d" "$SERVICE_FILE"
    echo "  - Removed 'EnvironmentFile' line (variables are now directly in ExecStart)."
fi

echo "Service file '$SERVICE_FILE' updated successfully."
echo ""

echo "3. Reloading systemd daemon and restarting service..."
sudo systemctl daemon-reload || { echo "ERROR: Failed to reload systemd daemon."; exit 1; }
sudo systemctl restart "$SERVICE_NAME" || { echo "ERROR: Failed to restart service. Check 'sudo systemctl status $SERVICE_NAME'."; exit 1; }

echo "Done."
echo "You can check the service status with: sudo systemctl status $SERVICE_NAME"
echo "You can view the service logs with: sudo journalctl -u $SERVICE_NAME --since '5 minutes ago'"
echo "Hotkey Engineer should now be able to access the keyring."
