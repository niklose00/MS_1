"""
------------------------------------------------------------------------------
File        : config.py
Description : Contains all global configuration constants for the discrete
              event simulation of a COVID-19 drive-in test station.
              These values define time durations, arrival rates, and capacity
              constraints used throughout the simulation.
Authors     : Simon Haebenbrock, Jonathan Stengl, Nico Klose
Group       : Group 6
------------------------------------------------------------------------------
"""

# Total simulation duration in seconds (2 hours)
SIMULATION_DURATION = 7200

# Time between car arrivals in seconds (uniform distribution)
ARRIVAL_INTERVAL = (30, 120)

# Duration of preregistration check in seconds (uniform distribution)
CHECK_DURATION = (60, 120)

# Time required to test one person in seconds (fixed)
TEST_DURATION_PER_PERSON = 240

# Maximum number of cars allowed in the test queue at any given time
MAX_QUEUE_SIZE = 10

# Maximum and minimum number of people per arriving car
MAX_PEOPLE_PER_CAR = 5
MIN_PEOPLE_PER_CAR = 1

# Controls whether event logs are printed to the console (True/False)
LOG_TO_CONSOLE = False

