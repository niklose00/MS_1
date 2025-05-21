"""
------------------------------------------------------------------------------
File        : stats.py
Description : Provides a lightweight class to track global simulation statistics,
              such as the number of cars tested, people tested, and cars rejected.
              These values are incremented during simulation events and later used
              for result analysis.
Authors     : Simon Haebenbrock, Jonathan Stengl, Nico Klose
Group       : Group 6
------------------------------------------------------------------------------
"""

class Statistics:
    """
    Tracks global counters used in the simulation for analysis and summary.
    Values are updated during event processing.
    """

    def __init__(self):
        """
        Initializes all statistic counters to zero.
        - total_cars: number of all cars that attempted to enter the system
        - tested_cars: number of cars that completed testing
        - tested_people: total number of individuals tested
        - rejected_cars: number of cars turned away due to full queue
        """
        self.total_cars = 0
        self.tested_cars = 0
        self.tested_people = 0
        self.rejected_cars = 0
