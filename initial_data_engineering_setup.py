'''
Created on Jun 29, 2024

@author: Charles Liles
'''

import sys
import pandas as pd
from google.cloud import bigquery
import pandas_gbq

from data_download_utilities import csv_download, bq_download, pull_and_merge_data
from missing_data_push import update_missing_data
    

def main(dl_year, state_fips_code, project_id, dataset_name, table_id):        
    merged_df = pull_and_merge_data(dl_year, state_fips_code)
    # We will now build the dataset and table for housing these data and put our data into it.
    # Construct a BigQuery client object.
    client = bigquery.Client()
    dataset_id = f'{project_id}.{dataset_name}'.format(client.project)
    
    # Construct a full Dataset object to send to the API.
    dataset = bigquery.Dataset(dataset_id)
    
    # Make sure the dataset will be deployed in the US region.
    dataset.location = "US"
    
    # Send the dataset to the API for creation, with an explicit timeout.
    # Will not raise a google.api_core.exceptions.Conflict if the Dataset already exists within the project.
    dataset = client.create_dataset(dataset, timeout=30, exists_ok=True)  # If the dataset exists from a previous run of this code, this should not error out.
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

    # Now build a table and push the merged_df data into it.  This will throw an error if the table already exists.
    table_id_combined = f'{dataset_name}.{table_id}'
    pandas_gbq.to_gbq(merged_df, table_id_combined, project_id=project_id, table_schema=[{'name': 'county_geom', 'type': 'GEOGRAPHY'}])
    
    # Update missing data.
    update_missing_data(state_fips_code, project_id, dataset_name, table_id)
    

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('Incorrect format, try again:\npython3 initial_data_engineering_setup.py [dl_year] [state_fips_code] [project_id] [dataset_name] [table_id]')
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])