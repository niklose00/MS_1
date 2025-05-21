"""
------------------------------------------------------------------------------
File        : event.py
Description : Defines the abstract base class Event and its concrete subclasses:
              ArrivingEvent, TestingEvent, and LeavingEvent. Each event
              represents a discrete step in the COVID-19 drive-in test process
              and is responsible for updating the simulation state and scheduling
              subsequent events.
Authors     : Simon Haebenbrock, Jonathan Stengl, Nico Klose
Group       : Group 6
------------------------------------------------------------------------------
"""

from abc import ABC, abstractmethod
from config import CHECK_DURATION, TEST_DURATION_PER_PERSON
from utils import uniform_int
from logger import Logger
import heapq


class Event(ABC):
    """
    Abstract base class for all event types in the simulation.
    Each event holds a timestamp, car ID, and number of passengers.
    Subclasses must implement the processEvent method.
    """

    def __init__(self, timestamp, car_id, num_people):
        self.timestamp = timestamp            # Time at which the event occurs
        self.car_id = car_id                  # Unique identifier for the car
        self.num_people = num_people          # Number of passengers in the car

    def __lt__(self, other):
        """
        Defines comparison for sorting events by timestamp in the event queue.
        Required for heapq-based scheduling.
        """
        return self.timestamp < other.timestamp

    @abstractmethod
    def processEvent(self, sim):
        """
        Abstract method to be implemented by all subclasses.
        Defines how the event affects the simulation.
        """
        pass


class ArrivingEvent(Event):
    """
    Represents the arrival of a car at the test station.
    If space is available in the queue, the car is added and a TestingEvent is scheduled.
    Otherwise, the car is rejected and logged accordingly.
    """

    def processEvent(self, sim):
        sim.stats.total_cars += 1

        # If queue is full, reject the car
        if len(sim.queue) >= sim.queue_limit:
            sim.stats.rejected_cars += 1
            sim.logger.log(self.timestamp, self.car_id, "Rejecting", len(sim.queue))
            return

        # Otherwise, add car to the queue and log arrival
        sim.queue.append(self)
        sim.logger.log(self.timestamp, self.car_id, "Arriving", len(sim.queue))

        # Schedule the testing event after preregistration check
        check_delay = uniform_int(*CHECK_DURATION)
        test_time = self.timestamp + check_delay
        sim.add_event(TestingEvent(test_time, self.car_id, self.num_people))


class TestingEvent(Event):
    """
    Represents the beginning of the COVID-19 test process for a car.
    The duration of the test depends on the number of people in the car.
    A LeavingEvent is scheduled after testing is complete.
    """

    def processEvent(self, sim):
        sim.logger.log(self.timestamp, self.car_id, "Testing", len(sim.queue))

        # Calculate total test duration and schedule the LeavingEvent
        test_duration = self.num_people * TEST_DURATION_PER_PERSON
        leave_time = self.timestamp + test_duration
        sim.add_event(LeavingEvent(leave_time, self.car_id, self.num_people))


class LeavingEvent(Event):
    """
    Represents the moment a car leaves the test station after testing.
    Updates simulation statistics and logs the departure.
    """

    def processEvent(self, sim):
        # Remove the car from the front of the queue
        sim.queue.pop(0)
        sim.stats.tested_cars += 1
        sim.stats.tested_people += self.num_people

        # Log the car leaving the system
        sim.logger.log(self.timestamp, self.car_id, "Leaving", len(sim.queue))
