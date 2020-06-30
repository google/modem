# Deploying BQML models

## Workflow Prerequisities: 

### Google Cloud Platform
1. **Enable Google Analytics API:** In the Cloud Console, ***APIs & Services > Library***, search for **Google Analytics API,** not the Google Analytics Reporting API.
2. **Create service account key:** In the Cloud Console, ***IAM & Admin > Service Accounts > Create Service Account***. Fill out the necessary details, such as service account name, service account email, creating & downloading the key file (additional permissions not needed). Please store the service account email & service key file safely. 
3. **Ensure that you have the right permissions to create the workflow:** At the very least, please request the following roles from the project admin. **If using Cloud Functions/Scheduler** - BigQuery Data Editor, BigQuery Job User, Cloud Functions Developer, Cloud Scheduler Admin, Service Account User. **If using Compute Engine** - BigQuery Data Editor, BigQuery Job User, Compute Admin, Service Account User. Also, ensure that your Compute Engine instance allows for 'Allow full access to all Cloud APIs'. (Compute Engine > "Select VM instance when stopped" > Edit > Cloud API access scopes > Allow full access to all Cloud APIs). Cheapest instance type: n1-micro.


### Google Analytics 
1. **Add the service account email as a user to Google Analytics:** Using the service account email generated from the previous step, create a user within ***Admin > Account > Account User Management*** with **Edit, Read and Analyze permissions**.
2. **Setup GA:** Create the custom dimensions. **If using Data Import, setup schema.** 

### Optional (for monitoring & logging)
1. **Setup logging for the workflow in BigQuery:** Set up a **BigQuery table with the schema** - *time TIMESTAMP, status STRING, error STRING*. To create a dataset with name 'workflow' and table name 'logs', please run the command below-
    ```
    DATASET_NAME="workflow" && TABLE_NAME="logs"
    bq mk --dataset $DATASET_NAME && bq mk --table $DATASET_NAME.$TABLE_NAME time:TIMESTAMP,status:STRING,error:STRING
    ```
2. **Setup email API for failure alerts:** Setup Sendgrid API by creating a free account and downloading an **API Key** in the Settings section of the [SendGrid UI](https://sendgrid.com/docs/for-developers/sending-email/authentication/).

<br>
<hr>

## Instructions:

### Model
If you wish to play around with BQML, feel free to use the sample code for a propensity model included [here](https://colab.research.google.com/github/google/modem/blob/master/bqml/model/BQML.ipynb).

**IMPORTANT:** Before proceeding, make sure you have your BQML predict query. 

### Pipeline

You can choose either option - 

#### A. BigQueryML models using Cloud Functions/Cloud Scheduler: *For interactive deployment instructions, click [here](https://colab.research.google.com/github/google/modem/blob/master/bqml/utils/BQML_Deployment_Template_Cloud_Function.ipynb).*

Otherwise, 

1. **Setup cloud function:** To create the cloud function, open a Cloud Shell and copy the following command. Follow the instructions that appear on the screen. When prompted, enter the GCP_PROJECT_ID and any desired name for your function.
    ```
    rm -rf modem && git clone https://github.com/google/modem.git && cd modem/bqml/pipeline && sh deploy.sh
    ```
    
2. **Edit 'svc_key.json' file:** Edit the created Cloud Function in the UI and update the svc_key.json file with the details from the downloaded service key file (check Prerequisites - Step 2).

3. **Edit 'params.py' file:** with the correct Google Analytics account id, property id, and dataset id. Also, update the query parameter with the BigQueryML predict query. ***Optionally***, you choose to enable monitoring and email, see the instructions in params.py file.

4. **Edit 'scheduler.sh' file:** with JOB_NAME, SCHEDULE, TIMEZONE, FUNCTION_URL & SERVICE_ACCOUNT_EMAIL as specified and "Deploy" the function. 

5. ***(OPTIONAL)* Test the cloud function:** To ensure that everything works okay before scheduling, test the Cloud function. **Note:** Please do not use the test functionality within the Cloud UI as the test functionality timeouts within 1 minute even if your function runs for longer. Use the following command in the shell instead - 
    ```
    curl <FUNCTION_URL> -H "Authorization: Bearer $(gcloud auth print-identity-token)" 
    ```

6. **Schedule the function using the Cloud Scheduler:** You can either use the Cloud Console (Cloud Scheduler > Create Job) or use the Cloud Shell by copying the commands from the edited 'scheduler.sh' file (lines 30 - 35).

#### B. BigQueryML models using Compute Engine/Shell: *For interactive deployment instructions, click [here](https://colab.research.google.com/github/google/modem/blob/master/bqml/utils/BQML_Deployment_Template_Compute_Engine.ipynb).*

Otherwise,

1. **Clone the repo:** SSH into Compute Engine and enter the following command. 
    ```
    sudo apt-get install git
    rm -rf modem && git clone https://github.com/google/modem.git && cd modem/bqml/pipeline 
    ```

2. **Edit 'svc_key.json' file:** Same as above (Step 2).

3. **Edit 'params.py' file:** Same as above (Step 3).

4. **Edit 'shell_scheduler.sh' file:** Edit line 19 with the desired cron schedule. 

5. **Test the code:** Run the command below. Check if a success message is displayed with the timestamp. 
   ```
   sh shell_deploy.sh
   ```
6. **Schedule the script:** Run the command below.
   ```
   sh shell_scheduler.sh
   ```
