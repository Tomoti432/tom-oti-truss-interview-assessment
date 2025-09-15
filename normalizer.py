#!/usr/bin/env python3

import sys
import csv
import logging
from datetime import datetime
from dateutil import parser  # helps read different date formats
from zoneinfo import ZoneInfo  # handles time zones (Python 3.9+)

# Show warnings in the terminal if something goes wrong
logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

# Set up time zones
PACIFIC = ZoneInfo("US/Pacific")
EASTERN = ZoneInfo("US/Eastern")

# This function turns a time like "01:23:45.678" into total seconds
def convert_duration(duration_text):
    try:
        hours, minutes, seconds = duration_text.split(":")
        sec_parts = seconds.split(".")
        whole_seconds = int(sec_parts[0])
        milliseconds = float("0." + sec_parts[1]) if len(sec_parts) > 1 else 0
        total_seconds = int(hours) * 3600 + int(minutes) * 60 + whole_seconds + milliseconds
        return total_seconds
    except:
        raise ValueError(f"Can't read duration: {duration_text}")

# This function cleans up one row of data
def clean_row(row):
    try:
        # Make the name all uppercase
        row["FullName"] = row["FullName"].upper()

        # Make sure ZIP code is 5 digits, add zeros if needed
        row["ZIP"] = row["ZIP"].zfill(5)

        # Read the date and time
        timestamp = parser.parse(row["Timestamp"])
        if not timestamp.tzinfo:
            timestamp = timestamp.replace(tzinfo=PACIFIC)
        else:
            timestamp = timestamp.astimezone(PACIFIC)
        # Convert to Eastern time and format nicely
        row["Timestamp"] = timestamp.astimezone(EASTERN).isoformat()

        # Convert durations to seconds
        foo_seconds = convert_duration(row["FooDuration"])
        bar_seconds = convert_duration(row["BarDuration"])
        row["FooDuration"] = str(foo_seconds)
        row["BarDuration"] = str(bar_seconds)

        # Add them together for TotalDuration
        row["TotalDuration"] = str(foo_seconds + bar_seconds)

        # Make sure Address and Notes are readable text
        row["Address"] = row["Address"].encode("utf-8", "replace").decode("utf-8")
        row["Notes"] = row["Notes"].encode("utf-8", "replace").decode("utf-8")

        return row
    except Exception as error:
        logging.warning(f"Skipping row because of error: {error}")
        return None

# This is the main part that runs when you start the script
def main():
    # Read the CSV file from input
    reader = csv.DictReader(sys.stdin)

    # Write the cleaned CSV to output
    writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames)
    writer.writeheader()

    for row in reader:
        cleaned = clean_row(row)
        if cleaned:
            writer.writerow(cleaned)

# Run the main function
if __name__ == "__main__":
    main()
