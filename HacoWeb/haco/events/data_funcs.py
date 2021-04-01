# Use requests for NASA archives
import requests
import datetime
import pandas as pd
from help_scripts.global_funcs import get_julian_date, get_home_dir, dpd_lon
from django.db import connection


# This function is for fetching most recent
# fire events from NASA MODIS Satellite
def modis_record_fetch():
    # Get the path
    file = get_home_dir()  # BASE DIR
    file += '/nasa_app_bearer.txt'  # Append key

    # Parameters for Request
    key = open(file, "r").read()  # Key Excluded from GIT
    headers = {
        "Authorization": f"Bearer {key}"
    }

    # MODIS Data Retrieval Entry Point
    url = "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content" \
          "/archives/FIRMS/c6/Global/MODIS_C6_Global_MCD14DL_NRT_"
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    # Get a Julian date
    today_julian = get_julian_date(date)
    url += str(today_julian)
    # Append .txt to string as formatted in archive
    url += str(".txt")
    r = requests.get(url, headers=headers)

    # Return data fetched
    return r.text


# Overwrites data in a local text file
def write_modis_data(data):
    # Function call to fetch new data
    file = get_home_dir()  # Get directory
    file += '/data/MODIS_C6_DATA_new.txt'  # Append new String to directory
    with open(file, mode='w',) as f:
        f.write(data)  # Write data to new file using Write mode which overwrites whatever there already
    data_to_csv()


# Simple Conversion Function to_csv using Pandas
def data_to_csv():
    file = get_home_dir()
    file += '/data/MODIS_C6_DATA_new.txt'
    data = pd.read_csv(file)
    file = get_home_dir() + "/data/MODIS_C6_DATA_new.csv"
    data.to_csv(file, mode='w')


# Used to define a Wildfire event in terms of this system
# to avoid duplicating multiple records with the same coordinates
# this will first check the records coordinates exist within the DB within a defined threshold.
# A threshold exists and is passable as a parameter to the function to allow it to be changed dynamically.
# The treshold (t) defines how much variance is permissable in the lon and lat coordinates for it to be considred
# a seperate event. There are no standards which really define this but it is practical to include such limitations
# on data being imported to avoid data redundancy and overpopulation of the database. Further, it allows events to
# be seperated from each other. The variance between a degree length of distance for longitude varies
# greatly as the latitude changes. The length of a degree of latitude does not differ much as the
# longitude changes and will be taken as the value of the length of a degree at the equator (69.172 miles)
def pre_db_process_data(event, *t):
    # Define default thresholds
    try:
        if not t:
            # Default thresholds
            t_lat = t_lon = 0.499
        else:
            # Threshold provided
            t_lat = t_lon = t

        # Calculate Distance per Degree
        v_lon_dpd = dpd_lon(event.lat)  # Expects a latitude and returns a distance per degree (dpd) float val
        c_lat_dpd = 69.172  # Constant... distance per degree at the equator for lat

        # Calculate Threshold Markers
        lon_variance = (v_lon_dpd * t_lon) / 100
        lat_variance = (c_lat_dpd * t_lat) / 100

        # Open connection cursor
        with connection.cursor() as c:

            c.execute(
                'SELECT * '
                'FROM events_event '
                'WHERE lat BETWEEN (%s-%s)::float8 '
                'AND (%s+%s)::float8 '
                'AND lon BETWEEN (%s-%s)::float8 '
                'AND (%s+%s)::float8 '

                # Query Parameters
                , [event.lat, lat_variance, event.lat, lat_variance, event.lon, lon_variance, event.lon, lon_variance]
            )
            # Grab next row
            row = c.fetchone()
            if row is None:
                return 1  # Row can be inserted

    except ValueError as e:
        raise ValueError(f'Value passed to fuction (dpd_lon()) invalid {e}')

    # Row is not inserted
    return 0
