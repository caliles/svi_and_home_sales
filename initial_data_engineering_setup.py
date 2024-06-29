'''
Created on Jun 29, 2024

@author: cl101
'''

import sys
import pandas as pd
from google.cloud import bigquery
import pandas_gbq

from data_download_utilities import csv_download, bq_download


def pull_and_prep_zillow_data(dl_year, state_fips_code = "All"):
    '''
    Pulls zillow data and preps it by averaging over the year of interest.  Also fixes issus with leading zeros being missing from FIPS codes.
    Args:
        dl_year: the year on which to subset the pulled data.
        state_fips_code: the fips code for the state of interest if there is one.
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
        if n[0:4] == '2020':
            print(n)
            months_to_avg_list.append(n)
    df_zillow['average'] = df_zillow[months_to_avg_list].mean(axis=1)
    # Need to drop State column to avoid a conflict in variable names when merging:
    df_zillow.drop('State', axis = 1, inplace = True)
    return df_zillow


def main(dl_year, state_fips_code, project_id, dataset_name, table_id):
    # Pull Zillow Data.  We will pull the lower 33 percentile (bottom tier) for the state of interest.
    df_st_zillow = pull_and_prep_zillow_data(dl_year, state_fips_code)
    
    # Pull Area Deprivation Index information by county for the state of interest.  Also pull county geometry information.
    adi_query = 'SELECT * FROM `bigquery-public-data.broadstreet_adi.area_deprivation_index_by_county` WHERE YEAR = '
    geo_query = 'SELECT * FROM `bigquery-public-data.geo_us_boundaries.counties`'
    if state_fips_code != 'All':
        adi_df = bq_download(f'{adi_query} {dl_year} AND state_fips_code = {state_fips_code}')
        geo_df = bq_download(f'{geo_query} where state_fips_code = "{state_fips_code}')
    else:
        adi_df = bq_download(f'{adi_query} {dl_year}')
        geo_df = bq_download(f'{geo_query}')
        
    # Merge dataframes on FIPS codes.  Use outer joins for datasets which may not have records for some FIPS codes.
    merged_df = pd.merge(geo_df, adi_df, on='county_fips_code', how = 'outer')
    merged_df = pd.merge(merged_df, df_st_zillow, on='county_fips_code', how = 'outer')
    
    # We now need to get rid of any columns that start with a number as BigQuery does not allow this for column naming.
    for n in merged_df.columns:
        if n[0].isdigit():
            print(f'Deleting {n} colummn.')
            merged_df.drop(n, axis = 1, inplace = True)
    
    # We will now build the dataset and table for housing these data and put our data into it.
    # Construct a BigQuery client object.
    client = bigquery.Client()
    dataset_id = f'{project_id}.{dataset_name}'.format(client.project)
    
    # Construct a full Dataset object to send to the API.
    dataset = bigquery.Dataset(dataset_id)
    
    # Make sure the dataset will be deployed in the US region.
    dataset.location = "US"
    
    # Send the dataset to the API for creation, with an explicit timeout.
    # Raises google.api_core.exceptions.Conflict if the Dataset already
    # exists within the project.
    dataset = client.create_dataset(dataset, timeout=30, exists_ok=True)  # If the dataset exists from a previous run of this code, this should not error out.
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

    # Now build a table and push the merged_df data into it.  This will throw an error if the table already exists.
    table_id_combined = f'{dataset_name}.{table_id}'
    pandas_gbq.to_gbq(merged_df, table_id_combined, project_id=project_id, table_schema=[{'name': 'county_geom', 'type': 'GEOGRAPHY'}])
    

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('Incorrect format, try again:\npython3 initial_data_engineering_setup.py [dl_year] [state_fips_code] [project_id] [dataset_name] [table_id]')
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])