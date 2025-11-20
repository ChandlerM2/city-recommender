import requests
import os
from dotenv import load_dotenv
import logging

filename='logs/census_extraction.log'

logging.basicConfig(
    filename = filename,
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    filemode = 'a')

#ACS1 2024 provides most recent single-year estimates for cities 65K+
CENSUS_URL = "https://api.census.gov/data/2024/acs/acs1"
MIN_POPULATION = 100000
STATE_FIPS_CODES = [1,2,4,5,6,8,9,10, 
               11,12,13,15,16,17,18,19,20, 
               21,22,23,24,25,26,27,28,29,30,
               31,32,33,34,35,36,37,38,39,40, 
               41,42,44,45,46,47,48,49,50,
               51,53,54,55,56]


def test_census_connection(): # this is a test fucntion to see if the api works and connects properly
    load_dotenv()
    api_key = os.getenv("CENSUS_API_KEY")
    
    if not api_key:
        raise ValueError("CENSUS_API_KEY not found in environment variables.")
    
    # B01003_001E: total population estimate
    params = {
        "get": "NAME,B01003_001E", 
        "for": "place:*", 
        "in": "state:47", 
        "key": api_key} 
    response = requests.get(CENSUS_URL, params=params)
     
    if response.status_code == 200:
        return "Connection Established Successfully"
    else:   
        return {"error": response.status_code,
                "message": response.text
                }



def extract_all_cities_populations():
    load_dotenv()
    api_key = os.getenv("CENSUS_API_KEY")
    if not api_key:
        logging.critical("CENSUS_API_KEY not found in environment variables.")
        raise ValueError("CENSUS_API_KEY not found in environment variables.")
        
    cities_above_100k = []

    logging.info("Starting extraction of city populations from Census API.")
    for fips_code in STATE_FIPS_CODES:
        clean_fip = str(fips_code).zfill(2)
        #this pulls the Cities
        params = {
            "get": "NAME,B01003_001E",
            "for": "place:*",
            "in": f"state:{clean_fip}",
            "key": api_key
        }
        response = requests.get(CENSUS_URL, params=params)

        print("success")
        if response.status_code == 200:
            cities = response.json()
            for city in cities[1:]: 
                if int(city[1])  > MIN_POPULATION:
                    cities_above_100k.append(city)
        else:
            logging.error(f"State {fips_code} → HTTP {response.status_code}: {response.text}")
    
    
    logging.info(f"Completed extraction - found {len(cities_above_100k)} cities above population {MIN_POPULATION}")
    
    return cities_above_100k




print(extract_all_cities_populations())