"""
------------------------------------------------------------------------------
File        : logger.py
Description : Provides a logging mechanism for the discrete event simulation.
              Records all relevant events with timestamps, car IDs, event types,
              and number of cars in the system. Supports console printing and
              CSV export for later analysis.
Authors     : Simon Haebenbrock, Jonathan Stengl, Nico Klose
Group       : Group 6
------------------------------------------------------------------------------
"""

import csv

class Logger:
    """
    Logger class for recording all events that occur during the simulation.
    Supports logging to memory, printing to the console, and exporting to CSV.
    """

    def __init__(self):
        """
        Initializes an empty list to store log entries.
        Each entry is a dictionary with timestamp, car ID, event type,
        and number of cars in the system at that time.
        """
        self.entries = []

    def log(self, timestamp, car_id, event_type, cars_in_system):
        """
        Adds a new entry to the log.

        Args:
            timestamp (int): The time when the event occurred
            car_id (int): Unique identifier of the car
            event_type (str): Type of the event (e.g., 'Arriving', 'Testing', 'Leaving', 'Rejecting')
            cars_in_system (int): Number of cars currently in the system
        """
        self.entries.append({
            'timestamp': int(timestamp),
            'car_id': car_id,
            'event_type': event_type,
            'cars_in_system': cars_in_system
        })

    def print_log(self):
        """
        Prints the entire event log to the console in a formatted table.
        """
        print("\nEvent Log:")
        print(f"{'Time':>5} | {'Car ID':>6} | {'Event':>10} | {'#Cars in System':>16}")
        print("-" * 45)
        for entry in self.entries:
            print(f"{entry['timestamp']:>5} | {entry['car_id']:>6} | {entry['event_type']:>10} | {entry['cars_in_system']:>16}")

    def save_to_csv(self, filename="event_log.csv"):
        """
        Saves the event log to a CSV file.

        Args:
            filename (str): Name of the output file (default: 'event_log.csv')
        """
        with open(filename, mode='w', newline='') as csvfile:
            fieldnames = ['timestamp', 'car_id', 'event_type', 'cars_in_system']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for entry in self.entries:
                writer.writerow(entry)

        # print(f"\nCSV log saved as '{filename}'")
