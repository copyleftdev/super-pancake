
# Super Pancake

Super Pancake is a collection of Python scripts designed to extract browsing history from popular web browsers, specifically Google Chrome and Mozilla Firefox. These scripts create a CSV output with URLs and their corresponding last visit dates.

## Features

- Extract browsing history from:
  - Google Chrome
  - Mozilla Firefox

- Convert browser-specific timestamps to human-readable date-time format.
- Handle locked databases, which typically occur when the browser is open.
- Export extracted data to CSV, named based on the machine's hostname and the timestamp of the extraction.

## Usage

1. Ensure you have Python 3.x installed.
2. Clone the repository or download the scripts.
3. Navigate to the directory containing the scripts.
4. Run the desired script:
    - For Chrome: `python chrome_artifact_collector.py`
    - For Firefox: `python firefox_artifact_collector.py`

This will generate a CSV in the same directory with the extracted history.

## Notes

- Always ensure you have proper permissions and user consent when accessing or modifying their data.
- Browsers may sometimes lock the history database, especially if they're running. The scripts have logic to handle this scenario, but for best results, consider closing the browser before running.
- Firefox may have multiple profiles. The script currently processes the primary profile found.
