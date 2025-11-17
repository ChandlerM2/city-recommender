import requests
import os
from dotenv import load_dotenv

#ACS1 2024 provides most recent single-year estimates for cities 65K+
CENSUS_URL = "https://api.census.gov/data/2024/acs/acs1"

def test_census_connection():
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
        return response.json()
    else:   
        return {"error": response.status_code,
                "message": response.text
                }

    


result = test_census_connection()

print(result[0:5])