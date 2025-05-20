from abc import ABC, abstractmethod
from config import CHECK_DURATION, TEST_DURATION_PER_PERSON, MAX_QUEUE_SIZE
from utils import uniform_int
import heapq

class Event(ABC):
    def __init__(self, timestamp, car_id, num_people):
        self.timestamp = timestamp
        self.car_id = car_id
        self.num_people = num_people

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    @abstractmethod
    def processEvent(self, sim):
        pass


class ArrivingEvent(Event):
    def processEvent(self, sim):
        sim.stats.total_cars += 1

        if len(sim.queue) >= MAX_QUEUE_SIZE:
            sim.stats.rejected_cars += 1
            return

        sim.queue.append(self)
        check_delay = uniform_int(*CHECK_DURATION)
        test_time = self.timestamp + check_delay
        sim.add_event(TestingEvent(test_time, self.car_id, self.num_people))


class TestingEvent(Event):
    def processEvent(self, sim):
        test_duration = self.num_people * TEST_DURATION_PER_PERSON
        leave_time = self.timestamp + test_duration
        sim.add_event(LeavingEvent(leave_time, self.car_id, self.num_people))


class LeavingEvent(Event):
    def processEvent(self, sim):
        sim.queue.pop(0)
        sim.stats.tested_cars += 1
        sim.stats.tested_people += self.num_people
