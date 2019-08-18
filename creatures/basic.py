import random


class Basic:

    def __init__(self, creature):
        # TODO: Add vision distance
        self.__food_this_turn = 0
        # TODO: Should size be a neg modifier on speed?
        # TODO: Should speed be linked to a trait?
        self.__speed = 8 if creature is None else creature.get_speed()
        self.__moves = 0
        # TODO: should some part of parent size be used?
        self.__size = 1
        self.__doing_this_turn = None
        # TODO: max age linked to a trait
        self.__current_age = 0
        self.__max_age = 20
        self.__rand = random.Random()

    def __lt__(self, other):
        return self.__speed < other.__speed

    def mutate(self):
        if self.__rand.randint(0, 1) > 0:
            self.__speed += 1
        else:
            self.__speed -= 1

    def get_age(self):
        return self.__current_age

    def increase_age(self):
        self.__current_age += 1

    def get_speed(self):
        return self.__speed

    def get_size(self):
        return self.__size

    def has_moves_left(self):
        return self.__moves > 0

    def reset_moves(self):
        self.__moves = self.__speed

    def reset_doing_this_turn(self):
        self.__doing_this_turn = None

    def read_food_this_turn(self):
        return self.__food_this_turn

    def update_food_this_turn(self, update_by):
        self.__food_this_turn += update_by

    def reset_food_this_turn(self):
        self.__food_this_turn = 0

    def grow(self):
        # TODO: Clip max size at a certain value
        # TODO: Maybe this could be a trait
        self.__size += (self.__food_this_turn / 2)

    def starve(self):
        if self.__food_this_turn < 1:
            if self.__size > 1:
                self.__size -= 1
            else:
                return True
        return False

    def old_age(self):
        return self.__current_age >= self.__max_age

    def take_move(self, main_grid, food_grid, current_x, current_y, grid_size):
        # TODO: Size effects - can eat smaller animals, run from big animals?
        x = current_x
        y = current_y

        if self.__food_this_turn < 2:
            x, y, good_move = self.__move_toward_food(food_grid, current_x, current_y, grid_size)
            if not good_move:
                x, y = self.__move_randomly(current_x, current_y, grid_size)
        else:
            if self.__doing_this_turn is None:
                others_x, others_y, others_good_move = self.__move_toward_other(
                    main_grid, current_x, current_y, grid_size)
                food_x, food_y, food_good_move = self.__move_toward_food(food_grid, current_x, current_y, grid_size)

                if others_good_move and not food_good_move:
                    # move to others
                    x = others_x
                    y = others_y
                    self.__doing_this_turn = "others"
                if food_good_move and not others_good_move:
                    # move to food
                    x = food_x
                    y = food_y
                    self.__doing_this_turn = "food"
                if food_good_move and others_good_move:
                    # TODO: Introduce a trait that is passed from parents and prioritises one of these actions
                    # random choice
                    if self.__rand.randint(0, 1) > 0:
                        x = others_x
                        y = others_y
                        self.__doing_this_turn = "others"
                    else:
                        x = food_x
                        y = food_y
                        self.__doing_this_turn = "food"
                if not food_good_move and not others_good_move:
                    # totally random
                    x, y = self.__move_randomly(current_x, current_y, grid_size)
            else:
                if self.__doing_this_turn is "others":
                    x, y, good_move = self.__move_toward_other(
                        main_grid, current_x, current_y, grid_size)
                else:
                    x, y, good_move = self.__move_toward_food(food_grid, current_x, current_y, grid_size)

                if not good_move:
                    x, y = self.__move_randomly(current_x, current_y, grid_size)

        self.__moves -= 1
        return x, y

    def __move_toward_other(self, grid, current_x, current_y, grid_size):
        if len(grid[current_x][current_y]) > 1:
            return current_x, current_y, True
        else:
            up_ok, down_ok, right_ok, left_ok = self.__check_move_bounds(current_x, current_y, grid_size)

            if up_ok:
                if len(grid[current_x][current_y + 1]) > 1:
                    return current_x, current_y + 1, True
                if left_ok:
                    if len(grid[current_x - 1][current_y + 1]) > 1:
                        return current_x - 1, current_y + 1, True
                if right_ok:
                    if len(grid[current_x + 1][current_y + 1]) > 1:
                        return current_x + 1, current_y + 1, True

            if left_ok:
                if len(grid[current_x - 1][current_y]) > 1:
                    return current_x - 1, current_y, True

            if right_ok:
                if len(grid[current_x + 1][current_y]) > 1:
                    return current_x + 1, current_y, True

            if down_ok:
                if len(grid[current_x][current_y - 1]) > 1:
                    return current_x, current_y - 1, True
                if left_ok:
                    if len(grid[current_x - 1][current_y - 1]) > 1:
                        return current_x - 1, current_y - 1, True
                if right_ok:
                    if len(grid[current_x + 1][current_y - 1]) > 1:
                        return current_x + 1, current_y - 1, True

            return current_x, current_y, False

    def __move_toward_food(self, food_grid, current_x, current_y, grid_size):
        if food_grid[current_x][current_y] > 0:
            return current_x, current_y, True
        else:
            up_ok, down_ok, right_ok, left_ok = self.__check_move_bounds(current_x, current_y, grid_size)

            if up_ok:
                if food_grid[current_x][current_y + 1] > 0:
                    return current_x, current_y + 1, True
                if left_ok:
                    if food_grid[current_x - 1][current_y + 1] > 0:
                        return current_x - 1, current_y + 1, True
                if right_ok:
                    if food_grid[current_x + 1][current_y + 1] > 0:
                        return current_x + 1, current_y + 1, True

            if left_ok:
                if food_grid[current_x - 1][current_y] > 0:
                    return current_x - 1, current_y, True

            if right_ok:
                if food_grid[current_x + 1][current_y] > 0:
                    return current_x + 1, current_y, True

            if down_ok:
                if food_grid[current_x][current_y - 1] > 0:
                    return current_x, current_y - 1, True
                if left_ok:
                    if food_grid[current_x - 1][current_y - 1] > 0:
                        return current_x - 1, current_y - 1, True
                if right_ok:
                    if food_grid[current_x + 1][current_y - 1] > 0:
                        return current_x + 1, current_y - 1, True

            return current_x, current_y, False

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

    @staticmethod
    def __check_move_bounds(current_x, current_y, grid_size):
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
