#!/bin/bash

APP_DIR="$(dirname "$(readlink -f "$0")")"
VENV_DIR="$APP_DIR/venv"
MAIN_SCRIPT="Repeat-Key-Helper.py"
HE_CONFIG_PATH="$HOME/.local/share/hotkey_engineer/config.json"

# System dependencies for X11 automation
SYSTEM_DEPENDENCIES="python3-venv python3-tk python3-dev scrot xclip xsel python3-pip"

install() {
    echo "--- Starting Repeat Key! Installation ---"
    
    # Check for Wayland
    if [[ "$XDG_SESSION_TYPE" == "wayland" ]]; then
        echo "⚠️  WARNING: Wayland detected!"
        echo "This tool uses PyAutoGUI, which requires an X11 session."
        echo "It will likely NOT work unless you switch to 'GNOME on Xorg' or 'Plasma (X11)' at login."
        echo ""
        read -p "Do you want to continue anyway? (y/n): " wayland_confirm
        [[ $wayland_confirm != [yY] ]] && exit 1
    fi

    echo "1. Installing system-level dependencies (requires sudo)..."
    sudo apt-get update
    sudo apt-get install -y $SYSTEM_DEPENDENCIES || { echo "ERROR: Failed system install."; exit 1; }

    echo "2. Setting up Virtual Environment..."
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR"
    fi

    echo "3. Installing Python packages..."
    "$VENV_DIR/bin/pip" install --upgrade pyautogui sv-ttk || { echo "ERROR: Failed pip install."; exit 1; }

    echo ""
    echo "--- Setup Complete! ---"
    echo "----------------------------------------------------------------"
    echo "FINAL STEP: Add to Hotkey Engineer"
    echo "----------------------------------------------------------------"
    echo "1. Copy the JSON block below:"
    echo ""
    cat <<EOF
    {
      "name": "Repeat Key Helper",
      "path": "$APP_DIR/$MAIN_SCRIPT",
      "args": [],
      "enabled": true,
      "run_on_startup": false,
      "run_hotkey": true,
      "hotkey": ["<ctrl>", "<alt>", "z"],
      "hotkey_action": "run",
      "needs_gui": true,
      "description": "Opens the Repeat Key automation interface."
    }
EOF
    echo ""
    echo "2. Paste it into your config file located at:"
    echo "   $HE_CONFIG_PATH"
    echo ""
    echo "3. Restart the Hotkey Engineer service:"
    echo "   systemctl --user restart hotkey-engineer.service"
    echo "----------------------------------------------------------------"
}

uninstall() {
    read -p "Remove the virtual environment and local settings? (y/n): " confirm
    if [[ $confirm == [yY] ]]; then
        rm -rf "$VENV_DIR"
        rm -f "$APP_DIR/settings.json"
        echo "Repeat Key! components removed."
    fi
}

if [ "$EUID" -eq 0 ]; then
    echo "ERROR: Please run as a normal user (no sudo)."
    exit 1
fi

echo "--- Repeat Key! Management ---"
echo "1) Install / Update"
echo "2) Uninstall"
read -p "Choice [1-2]: " choice

case $choice in
    1) install ;;
    2) uninstall ;;
    *) echo "Invalid choice." ;;
esac
