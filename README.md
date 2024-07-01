# U.S. Area Deprivation Index and Housing Prices

This repo is a data engineering pipeline designed to pull publicly available Zillow home value records, county geometry, and Area Deprivation Index (ADI) data, merge them into a pandas dataframe, and push these data into a Google Cloud BigQuery table.  The Google Cloud BigQuery table is designed to serve as a backend for a LookerStudio dashboard geospatial plot for both Zillow home values and ADI temporally and geospatially aligned.  Users wishing to gain access to the LookerStudio dashboard may request access from the author.  Users can then make a copy of the LookerStudio dashboard and connect it with their own BigQuery backend built by running the code in this repo.

This code is easiest to deploy within a Google Cloud environment.  Google Cloud accounts can be created with $300.00 of initial cloud costs paid by the vendor.  Initial deployment of this code did not exceed $10.00 in cloud costs.  The code was successfully developed and tested in Google Cloud with the repo deployed on a Vertex AI Jupyter notebook VM with the following VM image: **Tensorflow Enterprise 2.6 (with LTS Intel MKL-DNN/MKL) with Python 3.9**.  Python 3.9 is strongly recommended to successfully install and run this repo.  The VM size used for successful testing was an n1-standard-4 machine type with 100 GB of disk attached.  No accelerators (i.e. GPUs, TPUs) were required to run this code.

## Google Cloud Required APIs  
The foolowing Google Cloud APIs had to be activated within the test project to successfully deploy this repo.  This may require an Admin for the project to enable deployment.  

**BigQuery API**   
**Notebooks API** (optional: only needed if using Vertex AI notebook for deployment)  

## Installation

To install this repo run the below commands:

```
git clone https://github.com/caliles/svi_and_home_sales.git
cd svi_and_home_sales
pip3 install -r requirements.txt
```

## Running the Code for Initial Data Pull

Run the following command to execute the data pipeline.  You will need to substitute in values for the command line arguments which are denoted in brackets after the Python script.

```
python3 initial_data_engineering_setup.py [4-digit-year] [state-fsips-code] [google-cloud-project] [name-of-bigquery-dataset-for-data] [name-of-bigquery-table-for-data]
```

A description of the command line arguments for the above script is provided below:  

**[4-digit-year]** = a four digit year, recommend using **2020** as this is a known year with data in both Zillow home value index and ADI.  

**[state-fips-code]** = a two-digit state Federal Information Processing System (FIPS), i.e **48** for Texas.  Use **All** if you want to pull all records for all states.  

**[google-cloud-project]** = the Google Cloud project where you want to deploy the data.  This was tested in the same Google Cloud project where the data would reside.  

**[name-of-bigquery-dataset-for-data]** = the BigQuery dataset name in which you want your code to be hosted.  The code will build the dataset in BigQuery if it doesn't already exist.  

**[name-of-bigquery-table-for-data]** = the BigQuery table to where you want the code to push the data.  This has to be a new table not already in existence for the code to work properly.  

## Running the Code for Data Updates

Run the following command to periodically update the data in BigQuery.  You will need to substitute in values for the command line arguments which are denoted in brackets after the Python script.

```
python3 missing_data_push.py [state-fsips-code] [google-cloud-project] [name-of-bigquery-dataset-for-data] [name-of-bigquery-table-for-data]
```

A description of the commandline arguments for the above script is provided below:  

**[state-fips-code]** = a two-digit state Federal Information Processing System (FIPS), i.e **48** for Texas.  Use **All** if you want to pull all records for all states.  

**[google-cloud-project]** = the Google Cloud project where you want to deploy the data.  This has to be the original project created when initial_data_engineering_setup.py was run. 

**[name-of-bigquery-dataset-for-data]** = the BigQuery dataset name in which you want your code to be hosted.  This has to be the original dataset created when initial_data_engineering_setup.py was run. 

**[name-of-bigquery-table-for-data]** = the BigQuery table to where you want the code to push the data.  This has to be the original table created when initial_data_engineering_setup.py was run.  

## Notes on Data Updates

The previously mentioned command can be set up to run periodically via a cron job or perhaps as a Windows scheduled task.  Also, it could potentially be deployed to run as a Google Cloud Function triggered periodically by Cloud Scheduler; a very inexpensive means of deploying scheduled tasks in Google Cloud.


## LookerStudio Dashboard Copy and Deployment

To deploy the LookerStudio dashboard available here: https://lookerstudio.google.com/reporting/10d07cd7-0625-4fda-8469-b0c4439fe32a/page/7Mj4D using the BigQuery data engineered by the previously mentioned code, you will first need to gain permission to view the original dashboard from the author of this repo.  Once you have permission to view the dashboard, you will need to navigate to LookerStudio and first create a new data source by selecting **Create** and then **Data source** as pictured below:  

![Alt text](imgs/1.png?raw=true "Create a new LookerStudio data source")

Next, you will need to select **BigQuery** as the Google Connector.  

![Alt text](imgs/2.png?raw=true "Select BigQuery as the dataset source")

You will then need to select your projects name and then the BigQuery dataset and table where your engineered data has been deployed.  Then select **Connect** as seen below.  

**Note**: your project, dataset, and table names will be different from the ones shown in the image below.  

![Alt text](imgs/3.png?raw=true "Select the BigQuery project, dataset, and table")

Next, you will need to add some calculated fields to the dataset.  These are just used as aliases which look better on the final dashboard.  Select **ADD A FIELD** and then enter **Area Deprivation Index** for the Field Name and enter **area_deprivation_index_percent** for the Formula.  Repeat this process once again by entering **Average Zillow Housing Price** for Field Name and selecting **average** for the Formula.  Once saved, navigate back to the LookerStudio main page by selecting the Looker emblem at the top left part of the browser.

![Alt text](imgs/4.png?raw=true "Create calculated fields")

Now that your dataset is ready, go to the original dashboard that was shared with you by the author of this repo.  Select the more vert symbol (three vertically stacked dots in the top right of the browser) and then select ""Make a copy"".  Then, select the name of the new LookerStudio for **New Data Source** and select ""Copy Report"".

**Note**: it may take a few minutes for your newly created dataset to pop up in the **New Data Source** dropdown menu.

![Alt text](imgs/5.png?raw=true "Copy the original Dashboard")

You should be able to see the new copied dashboard now, although sometimes its fields are incorrect post copy as in the image below.  If this occurs, first single left click on the map.  If geo locations are incorrect, click on the value in the **Geospatial field** and make sure **county_geom** is selected as seen in the image below.  Also, ensure that **Average Zillow Housing Price** is selected for the **Size** field and **Area Deprivation Index** is selected for the **Color metric**.

![Alt text](imgs/6.png?raw=true "Update the geospatial field")

If everything appears correct, you should wind up with a dashboard looking like the one seen below:

![Alt text](imgs/7.png?raw=true "Final, correct result")

Please do not hesitate to reach out to the author if you have any issues with deployment.

## Citations:

Zillow Home Value Index (ZHVI) All Homes Bottom Tier Series available at: https://www.zillow.com/research/data/

Area Deprivation Index (ADI) provided by Broadstreet on Google Cloud Platform BigQuery at: https://console.cloud.google.com/marketplace/product/broadstreet-public-data/adi

Census Bureau US Boundaries on Google Cloud Platform BigQuery: https://console.cloud.google.com/marketplace/product/united-states-census-bureau/us-geographic-boundaries
