import sim


def run():

    simulation = sim.Sim(starting_pop=40, grid_size=20, mutation_rate=10)
    simulation.start()


if __name__ == "__main__":
    run()