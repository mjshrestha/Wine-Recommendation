import http.client
import json
import time
import sys
import collections
import csv
from geopy import GoogleV3
from geopy.exc import GeopyError

csv_name = 'winemag-data-185k-03272019.csv'
api_key = '' 

geocoder = GoogleV3(api_key=api_key)
request_count = 0
request_limit = 100000

country_index = 5
province_index = 8
region_index = 6

header_row = []
rows = []

location_cache = {}

def read_csv():
    global header_row
    with open(csv_name, encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                header_row = row
                line_count += 1
            else:
                rows.append(row)
                line_count += 1
        print(f'Processed {line_count} lines.')

def write_csv(rows):
    with open('out.csv', 'w', newline='', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(header_row)
        writer.writerows(rows)

def geocode_location(locationStr):
    global request_count
    request_count += 1
    return geocoder.geocode(query=locationStr, exactly_one=True)

def print_progress(current, total):
    print('----------------------')
    print(f'Percent Complete: {current/float(total) * 100}%')
    print(f'Requests Made: {request_count}')
    print(f'Cached Requests: {len(location_cache)}')
    print('----------------------')

read_csv()
header_row.extend(['latitude', 'longitude'])
counter = 0

aborted = False

for row in rows:
    row.extend(['', ''])
    locationStr = ', '.join(filter(None, [row[region_index], row[province_index], row[country_index]]))
    #print(f'Geocoding location: {locationStr}')
    if (locationStr in location_cache):
        googleLoc = location_cache[locationStr]
    else:
        try:
            time.sleep(0.05)
            googleLoc = geocode_location(locationStr)
        except GeopyError:
            print(f'Failed to geocode address: {locationStr}')
            print(GeopyError)
        if (not googleLoc):
            print(f'Location response empty for: {locationStr}')
            counter += 1
            continue
        else:
            location_cache[locationStr] = googleLoc
    row[-2] = googleLoc.latitude
    row[-1] = googleLoc.longitude
    if (counter % 100 == 0):
        print_progress(counter, len(rows))
    if (request_count >= request_limit):
        aborted = True
        break
    counter += 1

if aborted:
    print('----------------------')
    print(f'Request limit reached at row: {counter}')
    print('----------------------')

write_csv(rows)













