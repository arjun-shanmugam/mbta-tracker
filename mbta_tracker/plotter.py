from bokeh.plotting import figure, show

from mbta_tracker.system import System


class SystemPlotter:
    _system: System
    figure: figure

    def __init__(self, system: System):
        self._system = system
        self.figure = figure(title="MBTA Tracker")

        self._plot_links()
        self._plot_stations()


    def _plot_stations(self):
        for station in self._system.stations:
            alpha = 0.5 if station.map_color == 'black' else 1
            size = 10 if station.endpoint else 5
            self.figure.scatter(x=station.x, y=station.y, fill_color=station.map_color, alpha=alpha, size=size)
    def _plot_links(self):
        xs = [[x_source, x_target] for x_source, x_target in self._system.links[['x_source', 'x_target']].values]
        ys = [[y_source, y_target] for y_source, y_target in self._system.links[['y_source', 'y_target']].values]
        self.figure.multi_line(xs=xs, ys=ys, color='black')