import pandas as pd
import matplotlib.pyplot as plt

def analyze(logger_entries, sim_stats):
    df = pd.DataFrame(logger_entries)

    # 1. Durchschnittliche Personen pro Auto
    avg_people_per_car = sim_stats.tested_people / sim_stats.tested_cars if sim_stats.tested_cars else 0

    # 2. Durchschnittliche Autos im System (über alle Events)
    avg_cars_in_system = df['cars_in_system'].mean()

    # 3. Anzahl abgewiesener Autos
    rejected_cars = sim_stats.rejected_cars

    # 4. Reduktion durch höhere Queue-Kapazität → tbd

    print("\nAnalysis Results:")
    print(f"1. Avg. people per car: {avg_people_per_car:.2f}")
    print(f"2. Avg. cars in system: {avg_cars_in_system:.2f}")
    print(f"3. Cars rejected due to full queue: {rejected_cars}")

    # 1. VISUAL: Anzahl Fahrzeuge im System über Zeit (alle 5 Minuten)
    df['minute'] = (df['timestamp'] // 300) * 5
    time_bins = df.groupby('minute')['cars_in_system'].mean()

    plt.figure(figsize=(10, 5))
    time_bins.plot(kind='bar')
    plt.title("⏱Avg. cars in system per 5-minute interval")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Average # of cars in system")
    plt.tight_layout()
    plt.show()

    # 2. VISUAL: Verweildauer im System (Arrive → Leave)
    arrivals = df[df['event_type'] == 'Arriving'].set_index('car_id')
    leaves = df[df['event_type'] == 'Leaving'].set_index('car_id')

    joined = arrivals[['timestamp']].join(leaves[['timestamp']], lsuffix='_arrive', rsuffix='_leave')
    joined.dropna(inplace=True)  # Falls ein Auto nicht mehr rausgekommen ist
    joined['dwell_time'] = joined['timestamp_leave'] - joined['timestamp_arrive']

    plt.figure(figsize=(8, 5))
    plt.hist(joined['dwell_time'], bins=20, edgecolor='black')
    plt.title("Dwell time distribution")
    plt.xlabel("Time in system (seconds)")
    plt.ylabel("Number of vehicles")
    plt.tight_layout()
    plt.show()
