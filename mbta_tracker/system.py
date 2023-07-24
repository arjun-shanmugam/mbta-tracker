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
        station_data = pd.read_csv(path_to_station_data)[['station_id', 'name', 'x', 'y', 'stop_lat', 'stop_lon', 'endpoint', 'map_color']]
        self.stations = [Station(id, name, x, y, latitude, longitude, endpoint, map_color) for id, name, x, y, latitude, longitude, endpoint, map_color in
                         station_data.values]

        self.links = pd.read_csv(path_to_links_data)
        station_data = station_data.set_index('station_id')
        self.links.loc[:, ['x_source', 'y_source']] = station_data.loc[self.links['source_station'], ['x', 'y']].values
        self.links.loc[:, ['x_target', 'y_target']] = station_data.loc[self.links['target_station'], ['x', 'y']].values

        self._gtfs = GTFSRealtime(gtfs_realtime_url, None)
    def update_trains(self):
        self._gtfs.get_train_positions()
