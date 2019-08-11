import random
import creatures.basic as basic_creature


class Builder:

    def __init__(self, mutation_rate):
        self.__mutation_rate = mutation_rate
        self.__rand = random.Random()

    def build(self):
        new = basic_creature.Basic(None)
        if self.__rand.randint(1, 100) <= self.__mutation_rate:
            new.mutate()
        return new

    def build_offspring(self, creature):
        new = basic_creature.Basic(creature)
        if self.__rand.randint(1, 100) <= self.__mutation_rate:
            new.mutate()
        return new
