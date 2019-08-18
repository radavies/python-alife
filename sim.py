import random

import creatures.builder
import graphing.graph


class Sim:

    def __init__(self, starting_pop, grid_size, mutation_rate):
        self.__draw_map_graphs = False
        self.__draw_map_graphs_every_x_steps = 10
        self.__end_after_x_turns = 1000
        self.__starting_pop = starting_pop
        self.__grid_size = grid_size
        self.__grid = [[[] for x in range(self.__grid_size)] for y in range(self.__grid_size)]
        self.__food = [[0 for x in range(self.__grid_size)] for y in range(self.__grid_size)]
        self.__rand = random.Random()
        self.__creature_builder = creatures.builder.Builder(mutation_rate)
        self.__graph = graphing.graph.Graph()
        self.__turn_count = 0
        self.__total_creatures = 0
        self.__creatures_died = 0
        self.__creatures_born = 0
        self.__creatures_grow = 0
        self.__max_speed = -1000
        self.__min_speed = 1000
        self.__average_speed = 0
        self.__max_size = -1000
        self.__min_size = 1000
        self.__average_size = 0

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
            self.__food[x][y] += 1

    def __run_sim(self):
        go = True
        while go:
            self.__step()
            self.__turn_count += 1
            print(self.__turn_count)
            if self.__turn_count % self.__draw_map_graphs_every_x_steps is 0 and self.__draw_map_graphs:
                self.__graph.render_map_graph(self.__grid, self.__turn_count)
            if self.__turn_count >= self.__end_after_x_turns or self.__total_creatures < 1:
                go = False
        self.__graph.render_end_of_sim_graphs()

    def __step(self):
        self.__reset_creatures()
        self.__place_food()

        creatures_have_moves = True
        while creatures_have_moves:
            creatures_have_moves = self.__move_creatures()
            self.__creatures_eat()

        self.__do_end_of_step_changes()
        self.__evaluate_grid()
        self.__graph.update_stats(self.__total_creatures, self.__creatures_born,
                                  self.__creatures_died, self.__min_speed,
                                  self.__average_speed, self.__max_speed,
                                  self.__creatures_grow, self.__min_size,
                                  self.__average_size, self.__max_size)

    def __reset_creatures(self):
        for x in range(self.__grid_size):
            for y in range(self.__grid_size):
                if len(self.__grid[x][y]) > 0:
                    for creature in self.__grid[x][y]:
                        creature.reset_moves()
                        creature.reset_food_this_turn()
                        creature.reset_doing_this_turn()
                        creature.increase_age()

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
                            new_x, new_y = creature.take_move(self.__grid, self.__food, x, y, self.__grid_size)
                        self.__new_grid[new_x][new_y].append(creature)
        self.__grid = self.__new_grid
        return something_moved

    def __creatures_eat(self):
        for x in range(self.__grid_size):
            for y in range(self.__grid_size):
                if len(self.__grid[x][y]) > 0:
                    self.__grid[x][y].sort()
                    for creature in self.__grid[x][y]:
                        if self.__food[x][y] > 0:
                            self.__food[x][y] -= 1
                            creature.update_food_this_turn(1)

    def __do_end_of_step_changes(self):
        # TODO: Make the offspring bit better
        # TODO: Size / speed to effect food needs
        creatures_died = 0
        creatures_born = 0
        creatures_grow = 0

        for x in range(self.__grid_size):
            for y in range(self.__grid_size):
                if len(self.__grid[x][y]) > 0:
                    new_creatures = []
                    for creature in self.__grid[x][y]:
                        if creature.starve() or creature.old_age():
                            self.__grid[x][y].remove(creature)
                            creatures_died += 1
                        elif creature.read_food_this_turn() > 1 and len(self.__grid[x][y]) > 1:
                            new_creatures.append(self.__creature_builder.build_offspring(creature))
                        elif creature.read_food_this_turn() > 2:
                            creatures_grow += 1
                            creature.grow()
                    for new_creature in new_creatures:
                        creatures_born += 1
                        self.__grid[x][y].append(new_creature)

        self.__creatures_born = creatures_born
        self.__creatures_died = creatures_died
        self.__creatures_grow = creatures_grow

    def __evaluate_grid(self):
        total_creatures = 0
        max_speed = -1000
        min_speed = 1000
        average_speed = 0
        max_size = -1000
        min_size = 1000
        average_size = 0

        for x in range(self.__grid_size):
            for y in range(self.__grid_size):
                if len(self.__grid[x][y]) > 0:
                    for creature in self.__grid[x][y]:
                        total_creatures += 1
                        if creature.get_speed() < min_speed:
                            min_speed = creature.get_speed()
                        if creature.get_speed() > max_speed:
                            max_speed = creature.get_speed()
                        average_speed += creature.get_speed()

                        if creature.get_size() < min_size:
                            min_size = creature.get_size()
                        if creature.get_size() > max_size:
                            max_size = creature.get_size()
                        average_size += creature.get_size()
        if total_creatures > 0:
            average_speed = average_speed / total_creatures
            average_size = average_size / total_creatures
        else:
            average_speed = min_speed = max_speed = 0
            average_size = min_size = max_size = 0

        self.__total_creatures = total_creatures
        self.__max_speed = max_speed
        self.__min_speed = min_speed
        self.__average_speed = average_speed
        self.__max_size = max_size
        self.__min_size = min_size
        self.__average_size = average_size

