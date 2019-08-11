import random


class Basic:

    def __init__(self, creature):
        self.__food_this_turn = 0
        self.__speed = 8 if creature is None else creature.get_speed()
        self.__moves = 0
        self.__rand = random.Random()

    def __lt__(self, other):
        return self.__speed < other.__speed

    def mutate(self):
        if self.__rand.randint(0, 1) > 0:
            self.__speed += 1
        else:
            self.__speed -= 1

    def get_speed(self):
        return self.__speed

    def has_moves_left(self):
        return self.__moves > 0

    def reset_moves(self):
        self.__moves = self.__speed

    def read_food_this_turn(self):
        return self.__food_this_turn

    def update_food_this_turn(self, update_by):
        self.__food_this_turn += update_by

    def reset_food_this_turn(self):
        self.__food_this_turn = 0

    def take_move(self, main_grid, food_grid, current_x, current_y, grid_size):
        x = current_x
        y = current_y
        if self.__food_this_turn < 2:
            x, y = self.__move_toward_food(food_grid, current_x, current_y, grid_size)
        else:
            x, y = self.__move_toward_other(main_grid, current_x, current_y, grid_size)
        self.__moves -= 1
        return x, y

    def __move_toward_other(self, grid, current_x, current_y, grid_size):
        if len(grid[current_x][current_y]) > 1:
            return current_x, current_y
        else:
            up_ok, down_ok, right_ok, left_ok = self.__check_move_bounds(current_x, current_y, grid_size)

            if up_ok:
                if len(grid[current_x][current_y + 1]) > 1:
                    return current_x, current_y + 1
                if left_ok:
                    if len(grid[current_x - 1][current_y + 1]) > 1:
                        return current_x - 1, current_y + 1
                if right_ok:
                    if len(grid[current_x + 1][current_y + 1]) > 1:
                        return current_x + 1, current_y + 1

            if left_ok:
                if len(grid[current_x - 1][current_y]) > 1:
                    return current_x - 1, current_y

            if right_ok:
                if len(grid[current_x + 1][current_y]) > 1:
                    return current_x + 1, current_y

            if down_ok:
                if len(grid[current_x][current_y - 1]) > 1:
                    return current_x, current_y - 1
                if left_ok:
                    if len(grid[current_x - 1][current_y - 1]) > 1:
                        return current_x - 1, current_y - 1
                if right_ok:
                    if len(grid[current_x + 1][current_y - 1]) > 1:
                        return current_x + 1, current_y - 1

            return self.__move_randomly(current_x, current_y, grid_size)

    def __move_toward_food(self, food_grid, current_x, current_y, grid_size):
        if food_grid[current_x][current_y]:
            return current_x, current_y
        else:
            up_ok, down_ok, right_ok, left_ok = self.__check_move_bounds(current_x, current_y, grid_size)

            if up_ok:
                if food_grid[current_x][current_y + 1]:
                    return current_x, current_y + 1
                if left_ok:
                    if food_grid[current_x - 1][current_y + 1]:
                        return current_x - 1, current_y + 1
                if right_ok:
                    if food_grid[current_x + 1][current_y + 1]:
                        return current_x + 1, current_y + 1

            if left_ok:
                if food_grid[current_x - 1][current_y]:
                    return current_x - 1, current_y

            if right_ok:
                if food_grid[current_x + 1][current_y]:
                    return current_x + 1, current_y

            if down_ok:
                if food_grid[current_x][current_y - 1]:
                    return current_x, current_y - 1
                if left_ok:
                    if food_grid[current_x - 1][current_y - 1]:
                        return current_x - 1, current_y - 1
                if right_ok:
                    if food_grid[current_x + 1][current_y - 1]:
                        return current_x + 1, current_y - 1

            return self.__move_randomly(current_x, current_y, grid_size)

    def __move_randomly(self, current_x, current_y, grid_size):
        moved = False
        while not moved:
            move_x = self.__rand.randint(-1, 1)
            move_y = self.__rand.randint(-1, 1)
            new_x = current_x + move_x
            new_y = current_y + move_y

            if (0 <= new_x < grid_size) and (0 <= new_y < grid_size):
                current_x = new_x
                current_y = new_y
                moved = True

        return current_x, current_y

    def __check_move_bounds(self, current_x, current_y, grid_size):
        up_ok = False
        down_ok = False
        right_ok = False
        left_ok = False

        if current_y + 1 < grid_size:
            up_ok = True
        if current_y - 1 >= 0:
            down_ok = True
        if current_x + 1 < grid_size:
            right_ok = True
        if current_x - 1 >= 0:
            left_ok = True

        return up_ok, down_ok, right_ok, left_ok
