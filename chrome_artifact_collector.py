import os
import sqlite3
import datetime
import platform
import shutil
import time
import csv
import socket


def get_chrome_history_path():
    current_os = platform.system().upper()

    if current_os == "WINDOWS":
        return os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\History"
    elif current_os == "DARWIN":  # macOS
        return os.path.expanduser('~') + "/Library/Application Support/Google/Chrome/Default/History"
    elif current_os == "LINUX":
        return os.path.expanduser('~') + "/.config/google-chrome/Default/History"
    else:
        raise ValueError(f"Unsupported OS: {current_os}")


def get_csv_filename():
    # Get computer's name
    computer_name = socket.gethostname()
    # Get the current date and time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # Return the combined filename
    return f"{computer_name}_{current_time}.csv"


def get_chrome_history():
    original_path = get_chrome_history_path()

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
            cursor.execute("SELECT url, last_visit_time FROM urls")
            results = cursor.fetchall()

            # Write data to the CSV file
            with open(csv_filename, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["URL", "Last Visited"])  # Write header
                for url, last_visit_time in results:
                    # Convert Chrome's timestamp to a readable format
                    visit_time = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=last_visit_time)
                    writer.writerow([url, visit_time])

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
    get_chrome_history()
