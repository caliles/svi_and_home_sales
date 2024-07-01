# U.S. Area Deprivation Index and Housing Prices

This repo is a data engineering pipeline designed to pull publicly available Zillow housing price records, county geometry, and Area Deprivation Index (ADI) data, merge them into a pandas dataframe, and push these data into a Google Cloud BigQuery table which is designed to serve as a 

```
pip install requirements.txt
```


## Google Cloud Required APIs  
BigQuery API  
Cloud Build API  
Cloud Logging API  
Cloud Pub/Sub API  
Notebooks API (optional
Cloud Run Admin API

Deployment Notebook: Tensorflow Enterprise 2.6 (with LTS Intel MKL-DNN/MKL) with Python 3.9

## Citations:

Zillow Home Value Index (ZHVI) All Homes Bottom Tier Series available at: https://www.zillow.com/research/data/

Area Deprivation Index (ADI) provided by Broadstreet on Google Cloud Platform BigQuery at: https://console.cloud.google.com/marketplace/product/broadstreet-public-data/adi

Census Bureau US Boundaries on Google Cloud Platform BigQuery: https://console.cloud.google.com/marketplace/product/united-states-census-bureau/us-geographic-boundaries
