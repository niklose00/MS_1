"""
------------------------------------------------------------------------------
File        : analysis.py
Description : Evaluates simulation results based on the event log and statistics.
              Computes key metrics and visualizes system load and dwell times.
Authors     : Simon Haebenbrock, Jonathan Stengl, Nico Klose
Group       : Group 6
------------------------------------------------------------------------------
"""

import pandas as pd
import matplotlib.pyplot as plt

def analyze(logger_entries, sim_stats):
    """
    Analyzes the event log and simulation statistics.
    - Calculates average people per car, average cars in system, and rejections.
    - Plots system load over time and dwell time distribution.

    Args:
        logger_entries (list): Logged event entries from the simulation
        sim_stats (Statistics): Aggregated counters from the simulation
    """
    df = pd.DataFrame(logger_entries)

    # 1. Average people per tested car
    avg_people_per_car = sim_stats.tested_people / sim_stats.tested_cars if sim_stats.tested_cars else 0

    # 2. Average number of cars in the system across all timestamps
    avg_cars_in_system = df['cars_in_system'].mean()

    # 3. Total number of rejected cars
    rejected_cars = sim_stats.rejected_cars

    print("\nAnalysis Results:")
    print(f"1. Avg. people per car: {avg_people_per_car:.2f}")
    print(f"2. Avg. cars in system: {avg_cars_in_system:.2f}")
    print(f"3. Cars rejected due to full queue: {rejected_cars}")

    # 4. Plot: average number of cars in system per 5-minute interval
    df['minute'] = (df['timestamp'] // 300) * 5
    time_bins = df.groupby('minute')['cars_in_system'].mean()

    plt.figure(figsize=(10, 5))
    time_bins.plot(kind='bar')
    plt.title("⏱ Avg. cars in system per 5-minute interval")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Average # of cars in system")
    plt.tight_layout()
    plt.show()

    # 5. Plot: dwell time in the system per car (Arriving → Leaving)
    arrivals = df[df['event_type'] == 'Arriving'].set_index('car_id')
    leaves = df[df['event_type'] == 'Leaving'].set_index('car_id')

    joined = arrivals[['timestamp']].join(leaves[['timestamp']], lsuffix='_arrive', rsuffix='_leave')
    joined.dropna(inplace=True)  # Skip cars that never left
    joined['dwell_time'] = joined['timestamp_leave'] - joined['timestamp_arrive']

    plt.figure(figsize=(8, 5))
    plt.hist(joined['dwell_time'], bins=20, edgecolor='black')
    plt.title("⏳ Dwell time distribution")
    plt.xlabel("Time in system (seconds)")
    plt.ylabel("Number of vehicles")
    plt.tight_layout()
    plt.show()
