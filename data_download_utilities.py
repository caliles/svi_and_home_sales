'''
Created on Jun 28, 2024

@author: cl101
'''

import sys
import pandas as pd

def csv_download(url):
    '''
    TODO
    '''
    df = pd.read_csv(url)
    return df  


def main(url):
    print(url)
    zillow_df = csv_download(url)
    print(zillow_df)


if __name__ == '__main__':
    
    main(sys.argv[1])