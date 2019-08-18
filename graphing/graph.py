import plotly.graph_objects as go
from plotly.subplots import make_subplots


class Graph:

    def __init__(self):
        self.__total_creatures_log = []
        self.__creatures_born_log = []
        self.__creatures_died_log = []
        self.__min_speed_log = []
        self.__average_speed_log = []
        self.__max_speed_log = []
        self.__creatures_grow_log = []
        self.__min_size_log = []
        self.__average_size_log = []
        self.__max_size_log = []

    def update_stats(self, total_creatures, creatures_born, creatures_died,
                     min_speed, average_speed, max_speed, creatures_grow,
                     min_size, average_size, max_size):
        self.__total_creatures_log.append(total_creatures)
        self.__creatures_born_log.append(creatures_born)
        self.__creatures_died_log.append(creatures_died)
        self.__min_speed_log.append(min_speed)
        self.__average_speed_log.append(average_speed)
        self.__max_speed_log.append(max_speed)
        self.__creatures_grow_log.append(creatures_grow)
        self.__min_size_log.append(min_size)
        self.__average_size_log.append(average_size)
        self.__max_size_log.append(max_size)

    def render_end_of_sim_graphs(self):

        fig = make_subplots(
            rows=3, cols=1,
            # column_widths=[0.6, 0.4],
            row_heights=[0.33, 0.33, 0.33],
            specs=[[{"type": "scatter"}],
                   [{"type": "scatter"}],
                   [{"type": "scatter"}]])

        fig.add_trace(go.Scatter(
            y=self.__total_creatures_log,
            name="Total Creatures"
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            y=self.__creatures_died_log,
            name="Creatures Died"
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            y=self.__creatures_born_log,
            name="Creatures Born"
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            y=self.__creatures_grow_log,
            name="Creatures which grew"
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            y=self.__min_speed_log,
            name="Min Speed"
        ), row=2, col=1)

        fig.add_trace(go.Scatter(
            y=self.__average_speed_log,
            name="Average Speed"
        ), row=2, col=1)

        fig.add_trace(go.Scatter(
            y=self.__max_speed_log,
            name="Max Speed"
        ), row=2, col=1)

        fig.add_trace(go.Scatter(
            y=self.__min_size_log,
            name="Min Size"
        ), row=3, col=1)

        fig.add_trace(go.Scatter(
            y=self.__average_size_log,
            name="Average Size"
        ), row=3, col=1)

        fig.add_trace(go.Scatter(
            y=self.__max_size_log,
            name="Max Size"
        ), row=3, col=1)

        fig.update_layout(
            title_text="Creatures",
        )

        fig.show()

    def render_map_graph(self, grid, step_count):
        usable_grid = self.__convert_sim_grid_for_graphing(grid)
        fig = go.Figure(
            layout_title_text="Map"
        )
        fig.add_trace(go.Heatmap(z=usable_grid))
        fig.write_image("ui/map-graphs/map{}.jpg".format(step_count))

    @staticmethod
    def __convert_sim_grid_for_graphing(grid):
        grid_size = len(grid)
        new_grid = [[0 for x in range(grid_size)] for y in range(grid_size)]
        for x in range(grid_size):
            for y in range(grid_size):
                new_grid[x][y] = len(grid[x][y])
        return new_grid
