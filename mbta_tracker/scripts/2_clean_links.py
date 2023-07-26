import json

import pandas as pd

GREEN_LINE_ROUTE_INFORMATION = "../../data/raw/station-network_green_line.json"
NON_GREEN_LINE_ROUTE_INFORMATION = "../../data/raw/station-network.json"
CLEANED_STATION_DATA = "../../data/clean/stations.csv"
OUTPUT_DATA = "../../data/clean/links.csv"

links_dfs = []
for ROUTE_INFORMATION in [GREEN_LINE_ROUTE_INFORMATION, NON_GREEN_LINE_ROUTE_INFORMATION]:
    with open(ROUTE_INFORMATION) as route_information:
        data = json.load(route_information)
        nodes = pd.DataFrame().from_records(data['nodes'])
        links = pd.DataFrame().from_records(data['links'])
    origin_stations = nodes.loc[links['source']]['id'].reset_index(drop=True)
    destination_stations = nodes.loc[links['target']]['id'].reset_index(drop=True)
    links_dfs.append(pd.concat([origin_stations, destination_stations, links['line']], axis=1, ignore_index=True))

links_df = pd.concat(links_dfs, axis=0)

links_df.columns = ['source_station_id', 'target_station_id', 'line']

# manually add glx stations
lechmere_union_square = {'source_station_id': 'place-lech', 'target_station_id': 'place-unsqu'}
lechmere_east_somerville = {'source_station_id': 'place-lech', 'target_station_id': 'place-esomr'}
east_somerville_gilman_square = {'source_station_id': 'place-esomr', 'target_station_id': 'place-gilmn'}
gilman_square_magoun_square = {'source_station_id': 'place-gilmn', 'target_station_id': 'place-mgngl'}
magoun_square_ball_square = {'source_station_id': 'place-mgngl', 'target_station_id': 'place-balsq'}
ball_square_medford_tufts = {'source_station_id': 'place-balsq', 'target_station_id': "place-mdftf"}
link_records = [lechmere_union_square, lechmere_east_somerville, east_somerville_gilman_square, gilman_square_magoun_square, magoun_square_ball_square,
                ball_square_medford_tufts]
links_df = pd.concat([links_df, pd.DataFrame().from_records(link_records)], axis=0)

# express target and source stations with stop codes as well
station_df = pd.read_csv(CLEANED_STATION_DATA, index_col='station_id')
links_df.loc[:, 'source_stop_code'] = station_df.loc[links_df['source_station_id'], 'stop_code'].reset_index(drop=True)
links_df.loc[:, 'target_stop_code'] = station_df.loc[links_df['target_station_id'], 'stop_code'].reset_index(drop=True)

# add x, y coordinates and lat, long coordinates to links
links_df.loc[:, ['x_source', 'y_source']] = station_df.loc[links_df['source_station_id'], ['x', 'y']].values
links_df.loc[:, ['x_target', 'y_target']] = station_df.loc[links_df['source_station_id'], ['x', 'y']].values
links_df.loc[:, ['lon_source', 'lat_source']] = station_df.loc[links_df['source_station_id'], ['stop_lon', 'stop_lat']].values
links_df.loc[:, ['lon_target', 'lat_target']] = station_df.loc[links_df['source_station_id'], ['stop_lon', 'stop_lat']].values

links_df.to_csv(OUTPUT_DATA)