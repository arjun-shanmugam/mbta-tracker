import pandas as pd
import requests
import time
from protobuf_to_dict import protobuf_to_dict
from google.transit import gtfs_realtime_pb2


def get_single_train_position(feed_entity):
    train_data = {'train_id': feed_entity['id'],
                  'route_id': feed_entity['vehicle']['trip']['route_id'].lower(),
                  'stop_id': feed_entity['vehicle']['stop_id'],
                  'current_status': feed_entity['vehicle']['current_status'],
                  'longitude': feed_entity['vehicle']['position']['longitude'],
                  'latitude': feed_entity['vehicle']['position']['latitude']}
    if "Braintree" in train_data['stop_id']:
        train_data['stop_id'] = 38671
    elif "Oak Grove" in train_data['stop_id']:
        train_data['stop_id'] = 70036
    elif "Union Square" in train_data['stop_id']:
        train_data['stop_id'] = 70503
    elif "Alewife" in train_data['stop_id']:
        train_data['stop_id'] = 141
    elif "Forest Hills" in train_data['stop_id']:
        train_data['stop_id'] = 10642
    return train_data



class GTFSRealtime:
    _url: str = "https://api-v3.mbta.com"
    _MBTA_API_KEY: str

    def __init__(self, url: str, mbta_api_key: str):
        self._MBTA_API_KEY = mbta_api_key
        self._url = url
        self._feed = gtfs_realtime_pb2.FeedMessage()

    def get_train_positions(self):
        response = requests.get(self._url)
        self._feed.ParseFromString(response.content)
        feed = protobuf_to_dict(self._feed)
        positions = [get_single_train_position(feed_entity) for feed_entity in feed['entity'] if
                     feed_entity['vehicle']['trip']['route_id'] in ["Blue", "Red", "Orange", "Green-B", "Green-C",
                                                                    "Green-D",
                                                                    "Green-B"]]

        return pd.DataFrame.from_records(positions)
