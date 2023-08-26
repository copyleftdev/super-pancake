import os
import sqlite3
import datetime
import platform
import shutil
import time
import csv
import socket
import glob


def get_firefox_history_path():
    current_os = platform.system().upper()

    if current_os == "WINDOWS":
        profiles_path = os.path.expanduser('~') + r"\AppData\Roaming\Mozilla\Firefox\Profiles\\"

    elif current_os == "DARWIN":  # macOS
        profiles_path = os.path.expanduser('~') + "/Library/Application Support/Firefox/Profiles/"
    elif current_os == "LINUX":
        profiles_path = os.path.expanduser('~') + "/.mozilla/firefox/"
    else:
        raise ValueError(f"Unsupported OS: {current_os}")

    # Firefox may have multiple profiles, so we're taking the first one found.
    profile_dirs = [f for f in glob.glob(profiles_path + "*/places.sqlite")]
    if not profile_dirs:
        raise ValueError("No Firefox profile found.")

    return profile_dirs[0]


def get_csv_filename():
    # Get computer's name
    computer_name = socket.gethostname()
    # Get the current date and time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # Return the combined filename
    return f"{computer_name}_{current_time}.csv"
def get_firefox_history():
    original_path = get_firefox_history_path()

    # Create a temporary copy
    copy_path = original_path + ".temp"
    shutil.copy2(original_path, copy_path)

    # Get the name for the CSV file
    csv_filename = get_csv_filename()

    attempts = 5
    for _ in range(attempts):
        try:
            connection = sqlite3.connect(copy_path)
            cursor = connection.cursor()

            # Firefox's schema is different from Chrome's.
            cursor.execute("SELECT url, last_visit_date FROM moz_places")
            results = cursor.fetchall()

            # Write data to the CSV file
            with open(csv_filename, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["URL", "Last Visited"])  # Write header
                for url, last_visit_date in results:
                    if last_visit_date is not None:
                        # Convert Firefox's timestamp to a readable format
                        visit_time = datetime.datetime(1970, 1, 1) + datetime.timedelta(microseconds=last_visit_date)
                        writer.writerow([url, visit_time])
                    else:
                        writer.writerow([url, "No recorded visit date"])

            # Clean up: Close the connection and remove the temporary copy
            connection.close()
            os.remove(copy_path)
            break  # if successful, exit the loop

        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and _ < attempts - 1:  # Don't sleep on the last attempt
                time.sleep(1)  # wait for 1 second before retrying
            else:
                # If it's a different error or the last attempt also failed, raise the exception
                raise e


if __name__ == "__main__":
    get_firefox_history()
