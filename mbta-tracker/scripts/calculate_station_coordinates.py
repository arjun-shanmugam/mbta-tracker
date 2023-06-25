import pandas as pd

GREEN_LINE_STATION_COORDINATES = "../../data/raw/spider_green_line.json"
NON_GREEN_LINE_STATION_COORDINATES = "../../data/raw/spider.json"
OUTPUT_STATION_COORDINATES = "../../data/clean/station_coordinates.csv"

# read raw green line coordinates.
green_line_station_coordinates = pd.read_json(GREEN_LINE_STATION_COORDINATES).T
green_line_station_coordinates.columns = ['x', 'y']

# read raw non-green line coordinates.
non_green_line_station_coordinates = pd.read_json(NON_GREEN_LINE_STATION_COORDINATES).T
non_green_line_station_coordinates.columns = ['x', 'y']

# adjust non-green line coordinates so that they are not offset relative to other stations
for dimension in ['x', 'y']:
    # difference between coordinates of park street in the two datasets will give offset
    offset = (green_line_station_coordinates.loc['place-pktrm', dimension] -
              non_green_line_station_coordinates.loc['place-pktrm', dimension])
    non_green_line_station_coordinates.loc[:, dimension] = non_green_line_station_coordinates[dimension] + offset

station_coordinates = pd.concat([green_line_station_coordinates, non_green_line_station_coordinates],
                                axis=0)

# flip map vertically
station_coordinates['y'] = station_coordinates['y'].max() - station_coordinates['y']

# save cleaned data
station_coordinates.to_csv(OUTPUT_STATION_COORDINATES)
