from typing import List

from mbta_tracker.line import Line


class Station:
    _id: str
    name: str
    x: float
    y: float
    latitude: float
    longitude: float
    endpoint: bool
    map_color: str

    def __init__(self, station_id: str, name: str, x: float, y: float, latitude: float, longitude: float, endpoint: bool, map_color: str):
        self._id = station_id
        self.name = name
        self.x = x
        self.y = y
        self.latitude = latitude
        self.longitude = longitude
        self.endpoint = endpoint
        self.map_color = map_color
