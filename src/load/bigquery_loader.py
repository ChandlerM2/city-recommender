import os 
import bigquery_loader
from src.extract.census import extract_all_cities_populations
from extract import census 
import pandas as pd

# def BQ_connection_check() :
#     load_dotenv()
#     api_key = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
#     return api_key 

# print(BQ_connection_check())


def load_census_to_bigquery (census_data):
    
    #convert census data to dataframe with proper column names 
    
    census_df = pd.dataframe(extract_all_cities_populations())

    return census_df

