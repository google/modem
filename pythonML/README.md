# Deploying PythonML (scikit-learn, tensorflow, xgboost) models


## Workflow Prerequisities

### Google Cloud Platform
1. **Enable Google Analytics API:** In the Cloud Console, ***APIs & Services > Library***, search for **Google Analytics API,** not the Google Analytics Reporting API.
2. **Create service account key:** In the Cloud Console, ***IAM & Admin > Service Accounts > Create Service Account***. Fill out the necessary details, such as service account name, service account email, creating & downloading the key file (additional permissions not needed). Please store the service account email & service key file safely. 
3. **Ensure that you have the right permissions to create the workflow:** **If using Compute Engine** - BigQuery Data Editor, BigQuery Job User, Compute Admin, Service Account User, Storage Object Creator & Viewer, ML Engine Developer & Viewer. Also, ensure that your Compute Engine instance allows for 'Allow full access to all Cloud APIs'. (Compute Engine > "Select VM instance when stopped" > Edit > Cloud API access scopes > Allow full access to all Cloud APIs). Cheapest instance type: n1-micro.


### Google Analytics 
1. **Add the service account email as a user to Google Analytics:** Using the service account email generated from the previous step, create a user within ***Admin > Account > Account User Management*** with **Edit, Read and Analyze permissions**.
2. **Setup GA:** Create the custom dimensions. If using Data Import, setup schema. 

--------

## Instructions

### Model (Upload model to Google AI Platform)

***To view a complete end-to-end example from model creation to upload, click [here](http://colab.research.google.com/github/google/modem/blob/master/pythonML/model/Sample_Propensity_Model_AI_Platform_(sklearn).ipynb).***

If you have already trained your model, ensure that the RUNTIME_VERSION, FRAMEWORK (version), PYTHON_VERSION are compatible.
E.g., RUNTIME_VERSION = 1.15, FRAMEWORK = 'SCIKIT-LEARN' (0.20.4), PYTHON_VERSION = 3.7
1. **Download the model as a pickle file (model.pkl)**.
```
# my_model_obj = sklearn.linear_model.LogisticRegression()
with open('model.pkl', 'wb') as f:
  pickle.dump(my_model_obj,f)
```
2. **Upload the model to AI Platform** (after updating the parameters) -  
```
gsutil cp model.pkl $GCS_MODEL_DIRECTORY
gcloud ai-platform models create $MODEL_NAME --regions $REGION
gcloud ai-platform versions create $VERSION_NAME --model $MODEL_NAME  \
  --origin $GCS_MODEL_DIR --runtime-version=$RUNTIME_VERSION \
  --framework $FRAMEWORK --python-version=$PYTHON_VERSION
```
3. **Ensure that you've noted the following params for automation** - 

  * AI Platform model [AI_PLATFORM_MODEL_NAME]
  * AI Platform version name [AI_PLATFORM_VERSION_NAME]
  * BQ columns to be used as feature inputs to the model [MODEL_INPUT_COL_NAMES]
  * Mapping between BQ columns/AI Platform model outputs & import format (Data Import schema or Measurement Protocol hit parameters) [COLUMN_MAP].

Detailed instructions for MODEL_INPUT_COL_NAMES & COLUMN_MAP can be found in this Colab [here](http://colab.research.google.com/github/google/modem/blob/master/pythonML/model/Sample_Propensity_Model_AI_Platform_(sklearn).ipynb) under 'Automation with Modem - Parameter Specification' section.

### Pipeline

1. **Download code:** SSH into the Compute Engine VM and run the following command - 
```
sudo apt install git && rm -rf modem && git clone https://github.com/google/modem.git && cd modem/pythonML/pipeline
```
2. **If needed, edit 'main.py' file to add pre and post-processing logic:** Add the respective logic to the start of the functions - preprocess_features() and postprocess_output(). Check the comments in the file and/or [Colab example](http://colab.research.google.com/github/google/modem/blob/master/pythonML/model/Sample_Propensity_Model_AI_Platform_(sklearn).ipynb) under *'Automation with Modem - Modifying code to add pre and post processing logic'* section.

3. **Edit 'svc_key.json' file:** Update the svc_key.json file with the details from the downloaded service key file (check Prerequisites - Step 2).

4. **Edit 'params.py' file:** with the correct Google Analytics account id, property id, and dataset id. Also, update the GA-BQ dataset/table names, model input columns and mapping between columns. Finally, update the AI Platform model and version name from Step 1.

5. **Test the code:** by running the following command - 
```
sh test.sh
```
6. **Edit 'deploy.sh' file:** Edit the cron schedule to your desired frequency. 

7. **Setup the cron job:** by running the following command - 
```
sh deploy.sh
```
