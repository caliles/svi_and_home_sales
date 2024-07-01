'''
Created on Jun 28, 2024

@author: Charles Liles
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


def pull_and_prep_zillow_data(dl_year, state_fips_code):
    '''
    Pulls zillow data and preps it by averaging over the year of interest.  Also fixes issus with leading zeros being missing from FIPS codes.
    Args:
        dl_year: the year on which to subset the pulled data.
        state_fips_code: the fips code for the state of interest if there is one, if 'All' is input, will return all state records.
    Returns:
        df_zillow: a pandas dataframe with the prepped data.
    '''
    df_zillow = csv_download('https://files.zillowstatic.com/research/public_csvs/zhvi/County_zhvi_uc_sfrcondo_tier_0.0_0.33_sm_sa_month.csv?t=1719616688')
    # We will fix cases where leading zeros were not kept for the state and municipal Federal Information Processing System (FIPS) codes.
    df_zillow['StateCodeFIPS'] = df_zillow['StateCodeFIPS'].astype(str)
    df_zillow['MunicipalCodeFIPS'] = df_zillow['MunicipalCodeFIPS'].astype(str)
    df_zillow['StateCodeFIPS'] = df_zillow['StateCodeFIPS'].apply('{:0>2}'.format)
    df_zillow['MunicipalCodeFIPS'] = df_zillow['MunicipalCodeFIPS'].apply('{:0>3}'.format)
    if state_fips_code != 'All':
        df_zillow = df_zillow[df_zillow['StateCodeFIPS'] == state_fips_code]
    df_zillow['county_fips_code'] =  df_zillow['StateCodeFIPS'] + df_zillow['MunicipalCodeFIPS']
    months_to_avg_list = []
    for n in df_zillow.columns:
        if n[0:4] == dl_year:
            #print(n)
            months_to_avg_list.append(n)
    df_zillow['average'] = df_zillow[months_to_avg_list].mean(axis=1)
    # Need to drop State column to avoid a conflict in variable names when merging with other datasets:
    df_zillow.drop('State', axis = 1, inplace = True)
    return df_zillow


def pull_bigquery_data(dl_year, state_fips_code):
    '''
    Pulls both ADI and county geometry polygons from public BigQuery tables and returns them as dataframes.
    Args:
        dl_year: the year of data to pull for the ADI data.
        state_fips_code: the FIPS code of interest, if 'All' is input, will return all state records.
    Returns:
        adi_df: a pandas dataframe containing the ADI information.
        geo_df: a pandas dataframe containing the county geometry information.
    '''
    # Pull Area Deprivation Index information by county for the state of interest.  Also pull county geometry information.
    adi_query = 'SELECT * FROM `bigquery-public-data.broadstreet_adi.area_deprivation_index_by_county` WHERE YEAR ='
    geo_query = 'SELECT * FROM `bigquery-public-data.geo_us_boundaries.counties`'
    if state_fips_code != 'All':
        #print(f'{adi_query} {dl_year} AND state_fips_code = "{state_fips_code}"')
        adi_df = bq_download(f'{adi_query} {dl_year} AND state_fips_code = "{state_fips_code}"')
        geo_df = bq_download(f'{geo_query} where state_fips_code = "{state_fips_code}"')
    else:
        adi_df = bq_download(f'{adi_query} {dl_year}')
        geo_df = bq_download(f'{geo_query}')
    return adi_df, geo_df


def pull_and_merge_data(dl_year, state_fips_code):
    '''
    Pulls ADI, county geometry, and Zillow information and merges them into a dataframe.
    Args:
        dl_year: the year of data to pull for the ADI data.
        state_fips_code: the FIPS code of interest, if 'All' is input, will return all state records.
    Returns:
        merged_df: a pandas dataframe containing merged ADI, county geometry, and Zillow information.
    '''
    # Pull Zillow Data.  We will pull the lower 33 percentile (bottom tier) for the state of interest.
    df_st_zillow = pull_and_prep_zillow_data(dl_year, state_fips_code)
    adi_df, geo_df = pull_bigquery_data(dl_year, state_fips_code)
    # Merge dataframes on FIPS codes.  Use outer joins for datasets which may not have records for some FIPS codes.
    merged_df = pd.merge(geo_df, adi_df, on='county_fips_code', how = 'outer')
    merged_df = pd.merge(merged_df, df_st_zillow, on='county_fips_code', how = 'outer')
    
    # We now need to get rid of any columns that start with a number as BigQuery does not allow this for column naming.
    for n in merged_df.columns:
        if n[0].isdigit():
            #print(f'Deleting {n} colummn.')
            merged_df.drop(n, axis = 1, inplace = True)
    return merged_df
    

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