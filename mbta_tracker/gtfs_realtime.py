import requests
from typing import Union, List
import time
from protobuf_to_dict import protobuf_to_dict
from google.transit import gtfs_realtime_pb2
from joblib import Parallel, delayed


def get_single_train_position(feed_entity):
    if feed_entity['vehicle']['trip']['route_id'] in ["Blue", "Red", "Orange", "Green-B", "Green-C", "Green-D", "Green-B"]:
        return {'train_id': feed_entity['id'],
                'route_id': feed_entity['vehicle']['trip']['route_id'],
                'longitude': feed_entity['vehicle']['position']['longitude'],
                'latitude': feed_entity['vehicle']['position']['latitude']}
    else:
        return {}
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
        t1 = time.time()
        # positions = Parallel(n_jobs=1)(delayed(get_single_train_position)(feed_entity) for feed_entity in feed['entity'])
        positions = [get_single_train_position(feed_entity) for feed_entity in feed['entity']]
        t2 = time.time()
        print(t2-t1)
        print(positions)


