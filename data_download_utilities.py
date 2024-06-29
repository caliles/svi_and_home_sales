'''
Created on Jun 28, 2024

@author: cl101
'''

import requests
from svi_data import svi
print(requests.certs.where())
import json
import csv
import pandas as pd

def zillow_download():
    '''
    TODO
    '''
    url = 'https://files.zillowstatic.com/research/public_csvs/zhvi/County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1719616688'
    df = pd.read_csv(url)
    return df
    
        

def svi_download():
    '''
    TODO
    '''
    url = 'https://data.cdc.gov/api/views/48va-t53r/rows.csv'
    df = pd.read_csv(url)
    return df
    


def main():
    zillow_df = zillow_download()
    print(zillow_df)
    svi_df = svi_download()
    print(svi_df)

if __name__ == '__main__':
    main()