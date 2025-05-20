from simulation import Simulation
from analysis import analyze

def main():
    sim = Simulation()
    sim.run()
    
    analyze(sim.logger.entries, sim.stats)

if __name__ == "__main__":
    main()
