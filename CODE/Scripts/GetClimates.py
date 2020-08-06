import http.client
import json
import time
import sys
import collections
import csv
import numpy as np
from scipy import spatial
from geopy import distance
from geopy.exc import GeopyError
from math import *

climate_csv_name = 'climates.csv'
wine_csv_name = 'out.csv'

header_row = []
rows = []
climate_rows = []

latIndex = -2
lngIndex = -1

def load_wine_csv():
    global header_row
    with open(wine_csv_name, encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                header_row = row
            else:
                rows.append(row)
            line_count += 1

def load_climate_csv():
    with open(climate_csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            climate_rows.append(row)

def write_csv(rows):
    with open('climate_out.csv', 'w', newline='', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(header_row)
        writer.writerows(rows)

def get_distance(srcLatLng, targetLatLng):
    return distance.distance(srcLatLng, targetLatLng).miles

def parse_climate(val):
    if not val:
        return None
    if len(val == 2):
        return ['', '', '']

def print_progress(current, total):
    print('----------------------')
    print(f'Percent Complete: {current/float(total) * 100}%')
    print('----------------------')

print('Loading climate csv')
load_climate_csv()
print('Loading wine csv')
load_wine_csv()

header_row.extend(['main climate', 'precipitation', 'temperature'])
counter = 0

latRows = [float(i[0]) for i in climate_rows]
lngRows = [float(i[1]) for i in climate_rows]

coordinates = list(zip(latRows, lngRows))

print('building tree...')
tree = spatial.cKDTree(coordinates)

for row in rows:
    lat = row[latIndex]
    lng = row[lngIndex]

    if not lat or not lng:
        continue
    try:
        dd, ii = tree.query((float(lat), float(lng)), k=1)
    except:
        continue

    closestRow = climate_rows[ii]
    #print('found climate: ', closestRow[0], closestRow[1], closestRow[2])
    row.append(closestRow[2])

    if (counter % 100 == 0):
        print_progress(counter, len(rows))

    counter += 1

write_csv(rows)













