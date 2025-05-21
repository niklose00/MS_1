"""
------------------------------------------------------------------------------
File        : simulation.py
Description : Core class of the discrete event simulation for a COVID-19
              drive-in test station. Manages event scheduling, queueing,
              simulation timing, and logging.
Authors     : Simon Haebenbrock, Jonathan Stengl, Nico Klose
Group       : Group 6
------------------------------------------------------------------------------
"""

import heapq
from event import ArrivingEvent
from config import LOG_TO_CONSOLE, SIMULATION_DURATION, ARRIVAL_INTERVAL, MIN_PEOPLE_PER_CAR, MAX_PEOPLE_PER_CAR
from utils import uniform_int
from stats import Statistics
from logger import Logger


class Simulation:
    """
    Manages the discrete event simulation. Responsible for:
    - Generating and scheduling all initial events
    - Managing the event queue
    - Executing the simulation loop
    - Maintaining simulation statistics and logs
    """

    def __init__(self, queue_size=10):
        """
        Initializes simulation state:
        - event_list: priority queue (min-heap) of all scheduled events
        - queue: cars currently waiting in the test station
        - current_time: current simulation time
        - stats: tracks totals (arrivals, tested cars/people, rejections)
        - car_counter: incremental ID for each arriving car
        - logger: records event data for analysis and CSV export
        """
        self.queue_limit = queue_size
        self.event_list = []
        self.queue = []
        self.current_time = 0
        self.stats = Statistics()
        self.car_counter = 0
        self.logger = Logger()

    def add_event(self, event):
        """
        Adds a new event to the priority queue (min-heap) based on timestamp.

        Args:
            event: Event object (e.g., ArrivingEvent, TestingEvent, etc.)
        """
        heapq.heappush(self.event_list, event)

    def get_next_event(self):
        """
        Retrieves the next scheduled event (earliest timestamp) from the queue.

        Returns:
            Event object with the smallest timestamp.
        """
        return heapq.heappop(self.event_list)

    def initialize_events(self):
        """
        Generates all ArrivingEvents for the simulation based on
        uniformly distributed arrival intervals. Each car is assigned
        a random number of passengers (1–5).
        """
        arrival_time = 0
        while arrival_time <= SIMULATION_DURATION:
            num_people = uniform_int(MIN_PEOPLE_PER_CAR, MAX_PEOPLE_PER_CAR)
            self.car_counter += 1
            self.add_event(ArrivingEvent(arrival_time, self.car_counter, num_people))
            arrival_time += uniform_int(*ARRIVAL_INTERVAL)

    def run(self):
        """
        Runs the simulation:
        - Initializes the event queue with arrival events
        - Continuously processes the next scheduled event until no events remain
        - Logs all events and saves the final event log to a CSV file
        """
        self.initialize_events()

        while self.event_list:
            event = self.get_next_event()
            self.current_time = event.timestamp
            event.processEvent(self)

        # Output the full event log
        if LOG_TO_CONSOLE:
            self.logger.print_log()

        self.logger.save_to_csv("event_log.csv")
