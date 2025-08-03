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

