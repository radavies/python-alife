import plotly.graph_objects as go


class Graph:

    __total_creatures_log = []
    __creatures_born_log = []
    __creatures_died_log = []

    def __init__(self):
        pass

    def update_stats(self, total_creatures, creatures_born, creatures_died):
        self.__total_creatures_log.append(total_creatures)
        self.__creatures_born_log.append(creatures_born)
        self.__creatures_died_log.append(creatures_died)

    def render_graph(self):
        fig = go.Figure(
            layout_title_text="Total Creatures"
        )

        fig.add_trace(go.Bar(
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
