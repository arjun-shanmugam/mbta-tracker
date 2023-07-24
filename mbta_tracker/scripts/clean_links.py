import json

import pandas as pd

GREEN_LINE_ROUTE_INFORMATION = "../../data/raw/station-network_green_line.json"
NON_GREEN_LINE_ROUTE_INFORMATION = "../../data/raw/station-network.json"
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

links_df.columns = ['source_station', 'target_station', 'line']

# manually add glx stations
lechmere_union_square = {'source_station': 'place-lech', 'target_station': 'place-unsqu'}
lechmere_east_somerville = {'source_station': 'place-lech', 'target_station': 'place-esomr'}
east_somerville_gilman_square = {'source_station': 'place-esomr', 'target_station': 'place-gilmn'}
gilman_square_magoun_square = {'source_station': 'place-gilmn', 'target_station': 'place-mgngl'}
magoun_square_ball_square = {'source_station': 'place-mgngl', 'target_station': 'place-balsq'}
ball_square_medford_tufts = {'source_station': 'place-balsq', 'target_station': "place-mdftf"}
records = [lechmere_union_square, lechmere_east_somerville, east_somerville_gilman_square, gilman_square_magoun_square, magoun_square_ball_square,
           ball_square_medford_tufts]
links_df = pd.concat([links_df, pd.DataFrame().from_records(records)], axis=0)

links_df.to_csv(OUTPUT_DATA)