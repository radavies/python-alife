import plotly.graph_objects as go


class Graph:

    def __init__(self):
        self.__total_creatures_log = []
        self.__creatures_born_log = []
        self.__creatures_died_log = []
        self.__min_speed_log = []
        self.__average_speed_log = []
        self.__max_speed_log = []

    def update_stats(self, total_creatures, creatures_born, creatures_died, min_speed, average_speed, max_speed):
        self.__total_creatures_log.append(total_creatures)
        self.__creatures_born_log.append(creatures_born)
        self.__creatures_died_log.append(creatures_died)
        self.__min_speed_log.append(min_speed)
        self.__average_speed_log.append(average_speed)
        self.__max_speed_log.append(max_speed)

    def render_pop_graph(self):
        fig = go.Figure(
            layout_title_text="Creatures"
        )

        fig.add_trace(go.Scatter(
            y=self.__total_creatures_log,
            name="Total Creatures"
        ))

        fig.add_trace(go.Scatter(
            y=self.__creatures_died_log,
            name="Creatures Died"
        ))

        fig.add_trace(go.Scatter(
            y=self.__creatures_born_log,
            name="Creatures Born"
        ))

        fig.add_trace(go.Scatter(
            y=self.__min_speed_log,
            name="Min Speed"
        ))

        fig.add_trace(go.Scatter(
            y=self.__average_speed_log,
            name="Average Speed"
        ))

        fig.add_trace(go.Scatter(
            y=self.__max_speed_log,
            name="Max Speed"
        ))

        fig.update_layout(
            xaxis=go.layout.XAxis(
                title=go.layout.xaxis.Title(
                    text="Time Steps"
                )
            ),
            yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text="Number of Creatures"
                )
            )
        )
        fig.show()

    def render_map_graph(self, grid, step_count):
        usable_grid = self.__convert_sim_grid_for_graphing(grid)
        fig = go.Figure(
            layout_title_text="Map"
        )
        fig.add_trace(go.Heatmap(z=usable_grid))
        fig.write_image("map{}.jpg".format(step_count))

    def __convert_sim_grid_for_graphing(self, grid):
        grid_size = len(grid)
        new_grid = [[0 for x in range(grid_size)] for y in range(grid_size)]
        for x in range(grid_size):
            for y in range(grid_size):
                new_grid[x][y] = len(grid[x][y])
        return new_grid
