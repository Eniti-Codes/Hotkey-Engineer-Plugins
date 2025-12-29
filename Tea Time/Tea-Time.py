# Hotkey Engineer Plugins Tea Time - A simple but essential utility that sends you a reminder to drink tea (or take a break!) every 3600 seconds.
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

import os
import time

# --- Configuration ---
# Set the time interval between reminders in seconds.
# 3600 seconds = 1 hour
REMINDER_INTERVAL = 3600

# Set the title and message for the notification.
NOTIFICATION_TITLE = "☕ Tea Time!"
NOTIFICATION_MESSAGE = "It's time to take a break and have a cup of tea."

# Set the path to your sound file.
# Make sure to place a sound file (e.g., a .wav file) in the same directory as this script,
# or provide the full path to the file.
SOUND_FILE_PATH = "tea_pour.wav"

def send_notification_with_sound():
    """
    Plays a sound and then sends a desktop notification.
    """
    # 1. Play the custom sound
    # We use 'paplay', the PulseAudio sound player, which is standard on Linux Mint.
    # The command checks if the sound file exists before trying to play it.
    if os.path.exists(SOUND_FILE_PATH):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Playing sound: {SOUND_FILE_PATH}")
        os.system(f'paplay "{SOUND_FILE_PATH}"')
    else:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Warning: Sound file not found at {SOUND_FILE_PATH}. Skipping sound playback.")

    # 2. Send the desktop notification
    try:
        command = f'notify-send -i "dialog-information" -t 10000 "{NOTIFICATION_TITLE}" "{NOTIFICATION_MESSAGE}"'
        os.system(command)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Tea reminder notification sent.")
    except Exception as e:
        print(f"Error sending notification: {e}")

def main():
    """
    Main function to run the tea reminder loop.
    """
    print("Tea time alarm started. A notification and sound will occur every hour.")
    print("Press Ctrl+C to stop the script.")
    try:
        while True:
            send_notification_with_sound()
            time.sleep(REMINDER_INTERVAL)
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

