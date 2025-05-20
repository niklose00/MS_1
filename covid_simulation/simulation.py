import heapq
from event import ArrivingEvent
from config import SIMULATION_DURATION, ARRIVAL_INTERVAL, MIN_PEOPLE_PER_CAR, MAX_PEOPLE_PER_CAR
from utils import uniform_int
from stats import Statistics
from logger import Logger


class Simulation:
    def __init__(self):
        self.event_list = []
        self.queue = []
        self.current_time = 0
        self.stats = Statistics()
        self.car_counter = 0
        self.logger = Logger()

    def add_event(self, event):
        heapq.heappush(self.event_list, event)

    def get_next_event(self):
        return heapq.heappop(self.event_list)

    def initialize_events(self):
        arrival_time = 0
        while arrival_time <= SIMULATION_DURATION:
            num_people = uniform_int(MIN_PEOPLE_PER_CAR, MAX_PEOPLE_PER_CAR)
            self.car_counter += 1
            self.add_event(ArrivingEvent(arrival_time, self.car_counter, num_people))
            arrival_time += uniform_int(*ARRIVAL_INTERVAL)

    def run(self):
        self.initialize_events()

        while self.event_list:
            event = self.get_next_event()
            self.current_time = event.timestamp
            event.processEvent(self)

        self.stats.print_summary()
        self.logger.print_log()
        self.logger.save_to_csv("event_log.csv")

