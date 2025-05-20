import csv

class Logger:
    def __init__(self):
        self.entries = []

    def log(self, timestamp, car_id, event_type, cars_in_system):
        self.entries.append({
            'timestamp': int(timestamp),
            'car_id': car_id,
            'event_type': event_type,
            'cars_in_system': cars_in_system
        })

    def print_log(self):
        print("\nEvent Log:")
        print(f"{'Time':>5} | {'Car ID':>6} | {'Event':>10} | {'#Cars in System':>16}")
        print("-" * 45)
        for entry in self.entries:
            print(f"{entry['timestamp']:>5} | {entry['car_id']:>6} | {entry['event_type']:>10} | {entry['cars_in_system']:>16}")

    def save_to_csv(self, filename="event_log.csv"):
        with open(filename, mode='w', newline='') as csvfile:
            fieldnames = ['timestamp', 'car_id', 'event_type', 'cars_in_system']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for entry in self.entries:
                writer.writerow(entry)
        print(f"\nCSV log saved as '{filename}'")
