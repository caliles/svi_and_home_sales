'''
Created on Jun 28, 2024

@author: cl101
'''

import sys
import pandas as pd
from google.cloud import bigquery
import pandas_gbq

def csv_download(url):
    '''
    Pulls a CSV file from the web.  Designed primarily for pulling Zillow open information.
    Args:
        url: a full URL to the file to be downloaded.
    Returns:
        df: a pandas dataframe with the data pulled from the CSV at the URL.
    '''
    df = pd.read_csv(url)
    return df  


def bq_download(query):
    '''
    Pulls data from Google Cloud BigQuery based on a user's query.
    NOTE: the BigQuery API must be enabled in the Google Cloud project from which this script is run.  Also, this definition is designed to run from a VM where BigQuery authorization has already been setup.
        (i.e. a GCP Cloud Shell or a GCP AI Vertex Deep Learning instance with Python 3.9 and TensorFlow:2.6.
    Args:
        query: an SQL query for pulling data from BigQuery.
    Returns:
        df: a pandas dataframe containing the response of the query.
    '''
    df = pd.read_gbq(query)
    return df
    

def main():
    # Some simple test examples only to be run for testing when run as main.
    print('https://files.zillowstatic.com/research/public_csvs/zhvi/County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1719616688')
    zillow_df = csv_download('https://files.zillowstatic.com/research/public_csvs/zhvi/County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1719616688')
    print(zillow_df)
    print('Fetch BigQuery data.')
    df = bq_download('SELECT * FROM `bigquery-public-data.broadstreet_adi.area_deprivation_index_by_county` WHERE YEAR = 2020 AND state_fips_code = "48"')
    print(df)
    

if __name__ == '__main__':
    main()