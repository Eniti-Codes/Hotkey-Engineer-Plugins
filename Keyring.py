import keyring
import pyautogui
import time
import sys
import os # For checking secret-tool availability

# --- Configuration: Make sure these are accurate! ---
# Use the EXACT SERVICE_ID and USERNAME you set with secret-tool
# Example: SERVICE_ID = "com.mom.masterpassword"
# Example: USERNAME = "my_main_login"
SERVICE_ID = "Kindergarten.CaptainSauce" # <-- REPLACE It
USERNAME = "Mrs.Applegate" # <-- REPLACE It

# --- Helper functions (from our debugging journey) ---
def is_secret_tool_available():
    """Checks if the 'secret-tool' command is available on the system."""
    return os.system("which secret-tool > /dev/null 2>&1") == 0

def get_master_password_from_keyring():
    """Retrieves the master password from the keyring with robust error handling."""
    try:
        password = keyring.get_password(SERVICE_ID, USERNAME)

        if password:
            # Check for duplicated password string (our specific bug!)
            password_length = len(password)
            if password_length % 2 == 0 and password_length > 0:
                first_half = password[:password_length // 2]
                second_half = password[password_length // 2:]
                if first_half == second_half:
                    print("\n!!! WARNING: Detected a duplicated password string from keyring! !!!")
                    print("This means the password was stored twice (e.g., 'mypassmypass') in the keyring.")
                    print("SUGGESTION: You need to fix your stored password in the keyring.")
                    print("  1. In your terminal, you can delete the existing problematic entry:")
                    print(f"     secret-tool secret-tool delete service \"{SERVICE_ID}\" username \"{USERNAME}\"")
                    print(f"     (Confirm deletion when prompted, typically by typing 'y' or 'Y')")
                    print("  2. Then, re-add it carefully, entering your password ONLY ONCE:")
                    print(f"     secret-tool store --label=\"Hotkey Engineer Master Password\" service \"{SERVICE_ID}\" username \"{USERNAME}\"")
                    print("     (Enter your password carefully when prompted.)")
                    print("Exiting to prevent incorrect typing.")
                    return None # Indicate failure
            return password
        else:
            print("\n!!! ERROR: Password not found in keyring! !!!")
            print(f"Could not find a password for Service: '{SERVICE_ID}' and Username: '{USERNAME}'.")
            print("SUGGESTION: Please ensure your master password is correctly stored in your keyring.")
            print("  1. If you haven't stored it yet, add it using the terminal:")
            if is_secret_tool_available():
                print(f"     secret-tool store --label=\"Hotkey Engineer Master Password\" service \"{SERVICE_ID}\" username \"{USERNAME}\"")
                print("     (Then enter your password when prompted.)")
            else:
                print("     (You may need to install 'secret-tool' first, e.g., 'sudo apt install libsecret-tools')")
            print("  2. Ensure the SERVICE_ID and USERNAME variables in this Python script exactly match what you used above.")
            # --- NEW SUGGESTION FOR LIST-KEYS.PY ---
            print("\n--- If you're unsure of the exact IDs of your stored passwords ---")
            print("  Run the 'List-keys.py' script (provided separately) to inspect all your keyring entries:")
            print("  python3 List-keys.py")
            print("  Look for your password entry's 'Label' and then note its 'service' and 'username' attributes.")
            # --------------------
            return None

    except keyring.errors.NoKeyringError:
        print("\n!!! ERROR: No keyring backend found or configured! !!!")
        print("This script requires a keyring (like GNOME Keyring/KWallet) to be set up.")
        print("SUGGESTION: Ensure you have a desktop environment with a running keyring daemon (e.g., GNOME, KDE).")
        print("  If you're running headless, you might need to manually unlock your keyring.")
        return None
    except Exception as e:
        print(f"\n!!! UNEXPECTED ERROR during password retrieval: {e} !!!")
        print("This might indicate an issue with your keyring setup or permissions.")
        return None

# --- Main automation function ---
def automated_password_type():
    print("Attempting to retrieve and type master password...")
    password = get_master_password_from_keyring()

    if password:
        print("Password retrieved successfully. Please switch to your target application in 3 seconds.")
        time.sleep(3) # Give user time to focus on target application

        try:
            pyautogui.typewrite(password, interval=0.01) # Use a small interval for robustness
            print("Password typed directly into the active field.")
        except Exception as e:
            print(f"\n!!! ERROR: Failed to type password using pyautogui: {e} !!!")
            print("SUGGESTION: This might be due to your desktop environment, display server (Wayland vs Xorg), or system permissions.")
            print("  - Ensure your target application window is active and has an input field focused.")
            print("  - If on Wayland, pyautogui's typing might be limited or require additional setup (Xorg is generally more compatible for pyautogui).")
            print("  - Try restarting your session or computer if this suddenly stopped working.")
            return # Exit function if typing fails
    else:
        print("Automated password typing aborted due to previous errors.")

# --- Script execution starts here ---
if __name__ == "__main__":
    automated_password_type()
    # Explicitly exit to ensure a clean process termination in IDEs/hotkey tools
    sys.exit(0)