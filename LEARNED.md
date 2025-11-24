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

the return in our case is in a `["NAME", "B01003_001E", "state", "place"]`
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
| 201 | Created |
| 204 | Okay, but no content received back |
| 400 | Bad Request (invalid parameters or malformed query)  |
| 401 | Auth Failed |
| 404 | URL Not Found |
| 500 | Server error|
| 503 | service unavailable |
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


## Logging for Production

We use print statements in testing but once we start to think about dev environments we need to use the logging module. 

`DEBUG` - Detailed diagnostic information
`INFO` - Makes sure that things are working as planned
`WARNING` - Something unexpected happened, but the code still executed
`ERROR` - a real error happened that could cause a degraded feel of code quality
`CRITICAL` - enough of an issue to possibly crash a program

**At the top of your file make sure you configure how you want the logs to look**
```python 
logging.basicConfig(
    filename = "census-logging.log"
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    filemode = 'a'
)
```

## Google BigQuery

### **Differences from Traditional Databases:**
  
  - lives on Googles Cloud instead of an on prem physical server
  - google handles storage, backups, and scaling
  - analytical style queryes (scans millions of rows) - columnar format (instead of row based)
  - only pay for data stored and queries run

### **Storage Format**
  
  1. project level (the name of the project/ warehouse)
  2. dataset (database or schema) 
  3. table (where your actual data lives)

### **table types**

**Native Table:** the data is fully managed and backed up. It lives in GBQ storage and is queryable instantly. This is where you would load from the beginning

**External Table:** the data lives in Google Cloud or Google Sheets, BigQuery is used to query the data. This is generally slower due to little - no caching. We would use this is data changes constantly outside of bigquery. usally this is data that lives somewhere else **already**

**Materialized View:** a pre-computed query result stored as a table that refreshed automatically when source data changes, Faster queryies and cost storage. It's like a view table but just better

### **Partitioning and Clustering**
These optimize query performance for large datasets

***Partitioning:***

- Splits table into segments by a column (usually date)
- if you had a query like "Get data for 2024" only scans 2024 partition
- Reduces data scanned = faster + cheaper

***Clustering:***

- Sorts data by specified columns
- Queries filtering/sorting by those columns are faster


### Security: Using a Service Account 


1. Creates  a "robot account" (not a real user)
2. Download a JSON key file with credentials
3. Code uses that key file to authenticate
4. Service account only has BigQuery permissions (nothing else)

**Pros:**

- Works anywhere (local, server, scheduled jobs)
- Can be shared with team (not your personal account)
- Principle of least privilege (only BigQuery access)
- Production-ready pattern

**Cons:**

- Requires initial setup
- JSON key file is sensitive and needs proper storage

Therefore you set this in .env and never commit to any services

### Permissions Model

**Roles you can assign:**
- **BigQuery Admin:** Full control (create datasets, tables, delete everything)
- **BigQuery Data Editor:** Read/write data, create tables (can't delete datasets)
- **BigQuery Job User:** Run queries only
- **BigQuery Data Viewer:** Read-only




## Creating Your Service Account

### **Step 1: Go to IAM & Admin**

In Google Cloud Console:
1. Click hamburger menu (☰) top-left
   
2. Find "IAM & Admin" section
3. Click "Service Accounts"

**Step 2: Create Service Account**

1. Click "+ Create Service Account" at top
2. **Service account name:** `city-pipeline` (or whatever you want)
3. **Service account description:** "Data pipeline for city recommender project"
4. Click "Create and Continue"

**Step 3: Grant Permissions**

1. Click "Select a role" dropdown
2. Search for: "BigQuery Data Editor"
3. Select it
4. Click "Continue"
5. Skip optional "Grant users access" step
6. Click "Done"

**Step 4: Create JSON Key**

1. Find your new service account in the list
2. Click the three dots (⋮) on the right
3. Click "Manage keys"
4. Click "Add Key" → "Create new key"
5. Choose "JSON" format
6. Click "Create"
7. **A JSON file downloads to your computer**

**Step 5: Store the Key Securely**

Move that downloaded JSON file:
```
city-recommender/
├── credentials/
│   └── bigquery-key.json  ← Put it here
```

Add `credentials/` to your `.gitignore`:
```
# In .gitignore
credentials/