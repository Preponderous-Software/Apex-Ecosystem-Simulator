from simulation import Simulation


def createAndRunSimulation():
    simulation = Simulation()
    return simulation.run()

while createAndRunSimulation() == "restart":
    pass