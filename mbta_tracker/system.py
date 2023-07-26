from typing import List

import pandas as pd

from mbta_tracker.gtfs_realtime import GTFSRealtime
from mbta_tracker.station import Station
from google.transit import gtfs_realtime_pb2
import requests


class System:
    stations: List[Station]
    links: pd.DataFrame
    _gtfs: GTFSRealtime

    def __init__(self, path_to_station_data: str, path_to_links_data: str, gtfs_realtime_url: str):
        station_data = pd.read_csv(path_to_station_data)[
            ['station_id', 'name', 'x', 'y', 'stop_lat', 'stop_lon', 'endpoint', 'map_color']]
        self.stations = [Station(id, name, x, y, latitude, longitude, endpoint, map_color) for
                         id, name, x, y, latitude, longitude, endpoint, map_color in
                         station_data.values]

        self.links = pd.read_csv(path_to_links_data)

        self._gtfs = GTFSRealtime(gtfs_realtime_url, None)

    def project(self, p1, p2, p3: np.):

    def update_trains(self):
        train_positions = self._gtfs.get_train_positions()



