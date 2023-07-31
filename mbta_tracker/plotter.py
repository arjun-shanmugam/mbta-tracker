from bokeh.models import Label
from bokeh.plotting import figure, show

from mbta_tracker.system import System


class SystemPlotter:
    _system: System
    figure: figure

    def __init__(self, system: System):
        self._system = system
        self.figure = figure(title="MBTA Tracker")
        self.figure.sizing_mode = 'scale_height'
        self._plot_links()
        self._plot_stations()


    def _plot_stations(self):
        for station in self._system.stations:
            size = 10 if station.endpoint else 5
            text = Label(x=station.x, y=station.y, text=station.name, text_font_size='7px')
            self.figure.add_layout(text)
            self.figure.scatter(x=station.x, y=station.y, color=station.map_color, size=size)
    def _plot_links(self):
        xs = [[x_source, x_target] for x_source, x_target in self._system._links_data[['x_source', 'x_target']].values]
        ys = [[y_source, y_target] for y_source, y_target in self._system._links_data[['y_source', 'y_target']].values]
        self.figure.multi_line(xs=xs, ys=ys, color='black')