"""
------------------------------------------------------------------------------
File        : main.py
Description : Main entry point of the discrete event simulation program for
              a COVID-19 drive-in test station. This script initializes and
              runs the simulation and then performs statistical analysis and
              visualization based on the event log.
Authors     : Simon Haebenbrock, Jonathan Stengl, Nico Klose
Group       : Group 6
------------------------------------------------------------------------------
"""

from simulation import Simulation
from analysis import analyze

def main():
    """
    Main execution function.
    - Initializes the simulation
    - Runs the full discrete event simulation
    - Analyzes and visualizes results based on the event log and statistics
    """
    sim = Simulation()          # Create a new simulation instance
    sim.run()                   # Start the simulation (generates events and processes them)

    # Perform analysis on the collected event log and statistical data
    analyze(sim.logger.entries, sim.stats)

# Ensures this script only runs when executed directly (not when imported as a module)
if __name__ == "__main__":
    main()
