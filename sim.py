import random

import creatures.builder
import graphing.graph


class Sim:

    def __init__(self, starting_pop, grid_size, mutation_rate):
        self.__starting_pop = starting_pop
        self.__grid_size = grid_size
        self.__grid = [[[] for x in range(self.__grid_size)] for y in range(self.__grid_size)]
        self.__food = [[False for x in range(self.__grid_size)] for y in range(self.__grid_size)]
        self.__rand = random.Random()
        self.__creature_builder = creatures.builder.Builder(mutation_rate)
        self.__graph = graphing.graph.Graph()
        self.__turn_count = 0

    def start(self):
        self.__place_creatures()
        self.__place_food()
        self.__run_sim()

    def __place_creatures(self):
        for counter in range(self.__starting_pop):
            x = self.__rand.randint(0, self.__grid_size - 1)
            y = self.__rand.randint(0, self.__grid_size - 1)
            self.__grid[x][y].append(self.__creature_builder.build())

    def __place_food(self):
        for counter in range(self.__starting_pop * 2):
            x = self.__rand.randint(0, self.__grid_size - 1)
            y = self.__rand.randint(0, self.__grid_size - 1)
            self.__food[x][y] = True

    def __run_sim(self):
        go = True
        while go:
            go = self.__step()
            self.__turn_count += 1
            print(self.__turn_count)
            if self.__turn_count >= 1000:
                go = False
        self.__graph.render_graph()

    def __step(self):
        self.__reset_creatures()
        self.__place_food()

        creatures_have_moves = True
        while creatures_have_moves:
            creatures_have_moves = self.__move_creatures()
            self.__creatures_eat()

        is_creatures = self.__evaluate_grid()
        return is_creatures

    def __reset_creatures(self):
        for x in range(self.__grid_size):
            for y in range(self.__grid_size):
                if len(self.__grid[x][y]) > 0:
                    for creature in self.__grid[x][y]:
                        creature.reset_moves()
                        creature.reset_food_this_turn()

    def __move_creatures(self):
        self.__new_grid = [[[] for x in range(self.__grid_size)] for y in range(self.__grid_size)]
        something_moved = False
        for x in range(self.__grid_size):
            for y in range(self.__grid_size):
                if len(self.__grid[x][y]) > 0:
                    for creature in self.__grid[x][y]:
                        new_x = x
                        new_y = y
                        if creature.has_moves_left():
                            something_moved = True
                            new_x, new_y = creature.move_toward_food(self.__food, x, y, self.__grid_size)
                            creature.take_move()
                        self.__new_grid[new_x][new_y].append(creature)
        self.__grid = self.__new_grid
        return something_moved

    def __creatures_eat(self):
        for x in range(self.__grid_size):
            for y in range(self.__grid_size):
                if len(self.__grid[x][y]) > 0:
                    self.__grid[x][y].sort()
                    for creature in self.__grid[x][y]:
                        if self.__food[x][y]:
                            self.__food[x][y] = False
                            creature.update_food_this_turn(1)

    def __evaluate_grid(self):
        total_creatures = 0
        creatures_died = 0
        creatures_born = 0
        max_speed = -1000
        min_speed = 1000
        average_speed = 0

        for x in range(self.__grid_size):
            for y in range(self.__grid_size):
                if len(self.__grid[x][y]) > 0:
                    new_creatures = []
                    for creature in self.__grid[x][y]:
                        total_creatures += 1
                        if creature.get_speed() < min_speed:
                            min_speed = creature.get_speed()
                        if creature.get_speed() > max_speed:
                            max_speed = creature.get_speed()
                        average_speed += creature.get_speed()
                        if creature.read_food_this_turn() < 1:
                            self.__grid[x][y].remove(creature)
                            creatures_died += 1
                        elif creature.read_food_this_turn() > 1:
                            new_creatures.append(self.__creature_builder.build_offspring(creature))
                    for new_creature in new_creatures:
                        creatures_born += 1
                        self.__grid[x][y].append(new_creature)
        average_speed = average_speed / total_creatures
        self.__graph.update_stats(total_creatures, creatures_born, creatures_died, min_speed, average_speed, max_speed)
        return total_creatures + creatures_born > 0
