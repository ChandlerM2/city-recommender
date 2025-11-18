# Learning Documentation

## Purpose
This file documents concepts learned, architectural decisions, and problems encountered while building this project. It serves as both a learning journal and interview preparation resource.


## CENSUS REST API REQUEST
- they **aggregate based on geographic boundaries/areas** defined by a FIPS code
  - FIPS code designed by the **NIST** to ID states, counties, cities, and other geo areas
  - [TIGERweb](https://www.census.gov/data/developers/data-sets/TIGERweb-map-service.html) -> geolocation service -> FIPS code
  - address --> [Geocoder](https://www.census.gov/data/developers/data-sets/Geocoding-services.html) -> translates addressed into lat/long -> TIGERweb

REST API - a web endpoint that returns data by sending an HTTP request. The API then sends back some type of structured data (usually JSON)

Parameters are the filters you place on the API: `?param1=value1&param2=value2&param3=value3`

``` python 
import requests

url = "https://api.example.com/data"
params = {"city": "Nashville", "metric": "population"}
response = requests.get(url, params=params) # here the parameters are given above with city = Nashville
data = response.json()
```

The census data will be get, for, and key


Sometimes you have to use headers instead of paramerters so you get a: 

```python 
headers = {"Authorization": "Bearer token123"}
response = requests.get(url, headers=headers) 
```


response.status_code dictionary
------------------
| code | Reason |
|-----|---------|
| 200 | Success |
| 400 | Bad Request (invalid parameters or malformed query)  |
| 401 | Auth Failed |
| 404 | URL Not Found |
| 500 | Server error|
--------------------



***ACS5***: 5-year aggregated surveys covering ALL geographies. More reliable due to larger sample size. Standard for most analysis.

***ACS1***: published for geo's greater than 65k and is best for big cities, YoY trend analysis, and getting the **most up to date population numbers**

## Project: Census Extraction Function

### What We Built
A test function that authenticates with the Census API and extracts population data for all Tennessee places from ACS1 2024. Returns parsed JSON or error dictionary.

### Architecture Decision: ACS1 2024
**Why we chose this:**
I chose ACS1 over ACS5 because I wanted the most recent survey data. I know the project will only use cities over 100k meaning that ACS1 should work fine.

**Tradeoffs:**
Gains:
- More recent data
- quicker pull times as there are fewer cities

Losses:  
- granularity of data
- Less reliable than 5-year estimates for small population changes
- Won't capture cities below 65K population

### Key Concepts Applied
**Environment Variables (.env):**
these are set in a .env file and help to pull passwords or secret keys into the workspace without hardcoding them.

**Error Handling Pattern:**
The status code check ensures the request succeeded (200) before attempting to parse JSON. If the request failed (404, 500, etc.), the response might be HTML or plain text, which would crash the .json() method.

### Gotchas & Edge Cases
 - When entering the inputs for the params spaces cannot be between two objects. For instance `"NAME,B01003_001E"` is okay but `"NAME, B01003_001E"` is not.  