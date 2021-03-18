# Use requests for NASA archives
import requests
import datetime
from help_scripts.global_funcs import get_julian_date, get_home_dir


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
def write_data():
    data = modis_record_fetch()
    file = get_home_dir()
    file += '/hot_data/VIIRS_DATA_new.txt'
    with open(file, mode='w') as f:
        f.write(data)


# Process Data Using Pandas
def data_sense():
    import pandas as p
    file = get_home_dir()
    file += '/hot_data/VIIRS_DATA_new.txt'
    p.read_csv(file)
