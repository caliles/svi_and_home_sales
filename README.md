# U.S. Area Deprivation Index and Housing Prices

This repo is a data engineering pipeline designed to pull publicly available Zillow home value records, county geometry, and Area Deprivation Index (ADI) data, merge them into a pandas dataframe, and push these data into a Google Cloud BigQuery table which is designed to serve as a backend for a LookerStudio dashboard plotting both Zillow home values and ADI temporally and geospatially aligned.  Users wishing to gain access to the LookerStudio dashboard may request access from the author.  Users can then make a copy of the LookerStudio dashboard and connect it with their own BigQuery backend built by running this repo.

This code is easiest to deploy within a Google Cloud environment.  Google Cloud accounts can be created with $300.00 of initial cloud costs paid by the vendor.  Initial deployment of this code did not exceed $10.00 in cloud costs.  The code was successfully developed and tested in Google Cloud with the repo deployed on a Vertex AI Jupyter notebook with the following VM image: Deployment Notebook: **Tensorflow Enterprise 2.6 (with LTS Intel MKL-DNN/MKL) with Python 3.9**.  Python 3.9 is strongly recommended to successfully install and run this repo.

## Google Cloud Required APIs  
The foolowing Googl Cloud APIs had to be activated within the test project to successfully deploy this repo:  
BigQuery API   
Notebooks API (optional: only needed if using Vertex AI notebook for deployment)  

## Installation

```
pip install requirements.txt
```







## Citations:

Zillow Home Value Index (ZHVI) All Homes Bottom Tier Series available at: https://www.zillow.com/research/data/

Area Deprivation Index (ADI) provided by Broadstreet on Google Cloud Platform BigQuery at: https://console.cloud.google.com/marketplace/product/broadstreet-public-data/adi

Census Bureau US Boundaries on Google Cloud Platform BigQuery: https://console.cloud.google.com/marketplace/product/united-states-census-bureau/us-geographic-boundaries
