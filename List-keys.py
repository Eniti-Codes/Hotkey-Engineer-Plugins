# Hotkey Engineer Plugins List keys - Lists all keyring entries with their labels.
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

import secretstorage
import sys

def list_keyring_entries():
    """Lists all keyring entries with their labels, inferred schemas, and attributes."""
    try:
        connection = secretstorage.dbus_init()
        collection = secretstorage.get_default_collection(connection)

        if collection.is_locked():
            print("Keyring is locked. Attempting to unlock...")
            try:
                collection.unlock()
            except secretstorage.exceptions.CollectionLockedException:
                print("Failed to unlock keyring. Please unlock it manually (e.g., via Seahorse/Passwords and Keys application) and try again.")
                return False

            if collection.is_locked():
                print("Keyring remained locked after attempt. Please unlock it manually and try again.")
                return False
            print("Keyring unlocked successfully.")

        print("\n--- Listing Keyring Entries ---")
        print("Look for your desired password entry by its 'Label' (Description in Seahorse).")
        print("Note the 'service' and 'username' attributes for use in your main script.")
        print("If 'service'/'username' are absent or generic, it might be a Secure Note.")

        for item in collection.get_all_items():
            print("\n-------------------------------------------------")
            label = item.get_label()
            attributes = item.get_attributes()
            
            # Attempt to infer schema name for clarity
            schema_name = "Unknown or Implicit"
            try:
                if hasattr(item, 'schema') and item.schema:
                    schema_name = item.schema.get_property('name')
                elif 'xdg:schema' in attributes:
                     schema_name = attributes['xdg:schema']
                elif 'service' in attributes and 'username' in attributes:
                    schema_name = "org.freedesktop.Secret.Generic (inferred)"
                elif 'service' not in attributes and 'username' not in attributes:
                     schema_name = "org.gnome.keyring.Note (inferred)"
            except Exception:
                pass # Fallback to default schema_name if error occurs

            print(f"Label (Description in Seahorse): {label}")
            print(f"Inferred Schema: {schema_name}")
            
            print("Attributes:")
            if attributes:
                for key, value in attributes.items():
                    print(f"  - {key}: {value}")
            else:
                print("  (No specific attributes listed)")
            
            # --- OPTIONAL: Uncomment the following lines to print the actual secret ---
            # --- USE WITH EXTREME CAUTION IN SECURE ENVIRONMENTS ---
            # try:
            #     secret_value = item.get_secret().decode('utf-8')
            #     print(f"Secret Value: {secret_value}")
            # except Exception:
            #     print("Secret Value: (Could not retrieve or decode)")
            # --------------------------------------------------------------------------

    except secretstorage.errors.NoCollectionError:
        print("\nERROR: No default keyring collection found.")
        print("Please ensure your keyring (e.g., GNOME Keyring) is active and has a default collection (usually 'Login').")
        return False
    except secretstorage.exceptions.SecretServiceNotAvailableException:
        print("\nERROR: Secret Service not available. Ensure your keyring daemon is running.")
        print("This often happens if you're not logged into a desktop environment with a running keyring.")
        return False
    except Exception as e:
        print(f"\nAN UNEXPECTED ERROR OCCURRED: {e}")
        return False
    finally:
        if 'connection' in locals() and connection:
            connection.close()
    return True

if __name__ == "__main__":
    if not list_keyring_entries():
        sys.exit(1)
