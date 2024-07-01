'''
Created on Jun 30, 2024

@author: Charles Liles
'''

import sys
import pandas as pd
from google.cloud import bigquery
import pandas_gbq

from data_download_utilities import csv_download, bq_download, pull_and_merge_data


def update_missing_data(state_fips_code, project_id, dataset_name, table_id):
    '''
    This function queries Zillow and ADI records to determine years covered by both.  It then compares unique years against the current project's
    BigQuery table to see which years are missing in the project table which serves as the backend for the LookerStudio dashboard.  If any years are missing,
    It then pulls the missing year's data for Zillow and ADI and uploads them into the project's BigQuery table.
    Args:
        state_fips_code: the fips code for the state of interest if there is one, if 'All' is input, will return all state records.
        project_id: the GCP project ID where data will be updated
        dataset_name: the BigQuery dataset where data will be updated
        table_id: the BigQuery table within the dataset denoted above.
    '''
    # Get unique Zillow year Data
    url = 'https://files.zillowstatic.com/research/public_csvs/zhvi/County_zhvi_uc_sfrcondo_tier_0.0_0.33_sm_sa_month.csv?t=1719616688'
    zillow_df = csv_download(url)
    year_list = []
    for n in zillow_df.columns:
        if n[0:4].isdigit():
            if int(n[0:4]) not in year_list:
                year_list.append(int(n[0:4]))
    
    # Get unique ADI year Data
    adi_query = 'SELECT DISTINCT year FROM `bigquery-public-data.broadstreet_adi.area_deprivation_index_by_county`'
    adi_check_df = bq_download(adi_query)
    adi_list = adi_check_df['year'].to_list()
    
    # Find all years that are common to both the Zillow and ADI datasets
    adi_zillow_match_year_list = list(set(year_list).intersection(adi_list))
    
    # Find all unique 
    current_data_query = f'SELECT DISTINCT year FROM `{project_id}.{dataset_name}.{table_id}`'
    current_data_df = bq_download(current_data_query)
    current_yrs_list = current_data_df['year'].to_list()
    
    #Find any missing years, pull their data, and input them into the project's BigQuery table
    missing_year_list = list(set(adi_zillow_match_year_list) - set(current_yrs_list))
    print('Missing years:')
    print(missing_year_list)
    for n in missing_year_list:
        dl_year = str(n)
        merged_df = pull_and_merge_data(dl_year, state_fips_code)
        table_id_combined = f'{dataset_name}.{table_id}'
        pandas_gbq.to_gbq(merged_df, table_id_combined, project_id=project_id, table_schema=[{'name': 'county_geom', 'type': 'GEOGRAPHY'}], if_exists = 'append')


def main(state_fips_code, project_id, dataset_name, table_id):
    update_missing_data(state_fips_code, project_id, dataset_name, table_id)
    

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Incorrect format, try again:\npython3 missing_data_push.py [state_fips_code] [project_id] [dataset_name] [table_id]')
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])