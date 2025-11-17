# CENSUS REST API REQUEST
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
| 400 | Auth was successful but query is invalid |
| 401 | Auth Failed |
| 404 | URL Not Found |
| 500 | Server error|
--------------------



***ACS5***: every geography in the US and based on 5 years of aggregated surveys. this is best for populations of less than 65k  

***ACS1***: published for geo's greater than 65k and is best for big cities, YoY trend analysis, and getting the **most up to date population numbers**

