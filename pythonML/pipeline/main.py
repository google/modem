# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
from google.cloud import bigquery
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import datetime
import httplib2
import pandas as pd
import numpy as np
import params
import os
import warnings

GA_ACCOUNT_ID = params.GA_ACCOUNT_ID
GA_PROPERTY_ID = params.GA_PROPERTY_ID
GA_DATASET_ID = params.GA_DATASET_ID
GA_IMPORT_METHOD = params.GA_IMPORT_METHOD
GCP_PROJECT = params.GCP_PROJECT
BQ_DATASET_NEW_DATA = params.GA_BQ_DATASET_NAME
BQ_TABLE_NEW_DATA = params.GA_BQ_TABLE_NAME
AI_PLATFORM_MODEL_NAME = params.AI_PLATFORM_MODEL_NAME
AI_PLATFORM_VERSION_NAME = params.AI_PLATFORM_VERSION_NAME
BQ_PREDICTION_FEATURES = params.MODEL_INPUT_COL_NAMES
CSV_COLUMN_MAP = params.COLUMN_MAP

SERVICE_ACCOUNT_FILE = "svc_key.json"
CLOUD_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
CSV_LOCATION = "output.csv"
GA_SCOPES = ['https://www.googleapis.com/auth/analytics.readonly',
             'https://www.googleapis.com/auth/analytics.edit',
             'https://www.googleapis.com/auth/analytics']
GA_API_NAME = 'analytics'
GA_API_VERSION = 'v3'

warnings.simplefilter(action='ignore', category=FutureWarning)

def authorize_ga_api():
  """Fetches the GA API obj.
  Returns:
    ga_api: GA API obj.
  """
  ga_credentials = ServiceAccountCredentials.from_json_keyfile_name(
      SERVICE_ACCOUNT_FILE, GA_SCOPES)
  http = ga_credentials.authorize(http=httplib2.Http())
  ga_api = discovery.build(GA_API_NAME, GA_API_VERSION, http=http)
  return ga_api

  
def read_new_data_from_bq():
  """Reads the prediction query from Bigquery using BQML.
  Returns:
    dataframe: BQML model results dataframe.
  """
  client = bigquery.Client()
  query = "SELECT * FROM `{0}.{1}.{2}`".format(GCP_PROJECT,
                                               BQ_DATASET_NEW_DATA,
                                               BQ_TABLE_NEW_DATA)
  query_job = client.query(query)
  results = query_job.result()
  dataframe = results.to_dataframe()
  return dataframe

  
def preprocess_features(df):
  """Preprocesses model input columns.
  Args:
    df: dataframe of input dataset, read from BQ.
  Returns:
    features: pre-processed model input columns.
    df: dataframe of input dataset, read from BQ.
  """
  # TODO(developer): If needed, add preprocessing logic.
  # The design principle to keep in mind is to always
  # add columns to the output dataframe,
  # even for intermediate outputs if necessary.
  # -------- Additional lines start here -------- 
  # -------- Additional lines end here ---------- 
  selected_df = df[BQ_PREDICTION_FEATURES] 
  features = selected_df.values.tolist()
  if np.array(features).shape == 1:
    features = [[f] for f in features]
  return features, df

  
def predict_using_ai_platform(feature_batch):
  """Fetches model predictions from AI Platform model. 
  Args:
    feature_batch: features in one batch.
  Returns:
    predictions: model predictions or error.
  """
  ai_platform = discovery.build("ml", "v1")
  name = 'projects/{}/models/{}/versions/{}'.format(GCP_PROJECT,
                                                    AI_PLATFORM_MODEL_NAME,
                                                    AI_PLATFORM_VERSION_NAME)
  response = ai_platform.projects().predict(name=name,
                                            body={'instances':
                                                  feature_batch}).execute()
  if 'error' in response:
      return ['error']*len(feature_batch)     
  return response['predictions']

def predict_model_output(features, dataframe):
  """Batches input features and fetches model predictions. 
  Args:
    features: pre-processed model input columns.
    dataframe: dataframe of input dataset, read from BQ.
  Returns:
    dataframe: appended dataframe with the predictions.
  """
  BATCH_SIZE = 2000
  predictions = []
  for batch_start_row in range(0, len(features), BATCH_SIZE):
    feature_batch = features[batch_start_row:batch_start_row+BATCH_SIZE]
    feature_predictions = predict_using_ai_platform(feature_batch)
    predictions = predictions + feature_predictions
  dataframe['predicted'] = predictions
  dataframe = dataframe[dataframe['predicted'] != 'error']
  return dataframe
  
def postprocess_output(df):
  """Post-process model predictions.
  Args:
    df: dataframe appended with predictions - ('predicted' column)
  Returns:
    df: dataframe with relevant & processed columns for GA import. 
  """
  predictions = df['predicted']
  # TODO(developer): If needed, add postprocessing logic. 
  # Mostly necessary if using custom prediction routine.
  # The design principle to keep in mind is to always
  # add columns to the output dataframe,
  # even for intermediate outputs if necessary.
  # -------- Additional lines start here -------- 
  # -------- Additional lines end here ----------  
  final_cols = list(CSV_COLUMN_MAP.keys())
  df = df[final_cols]
  df.columns = [CSV_COLUMN_MAP[bq_col_header] for bq_col_header in final_cols]
  return df
 

def prepare_csv(df):
  """Converts results dataframe to CSV.
  
  Args:
    df: final results dataframe for GA export.
  """
  csv_string = df.to_csv(index=False)
  with open(CSV_LOCATION, "w+") as f:
      f.write(csv_string)


def write_to_ga_via_di(ga_api):
  """Write the prediction results into GA via data import.
  Args:
    ga_api: Google Analytics Management API object.
  """
  media = MediaFileUpload(CSV_LOCATION,
                          mimetype="application/octet-stream",
                          resumable=False)
  ga_api.management().uploads().uploadData(
      accountId=GA_ACCOUNT_ID,
      webPropertyId=GA_PROPERTY_ID,
      customDataSourceId=GA_DATASET_ID,
      media_body=media).execute()
    
def delete_ga_prev_uploads(ga_api):
  """Delete previous GA data import files.
  Args:
    ga_api: Google Analytics Management API object.
  """
  response = ga_api.management().uploads().list(
      accountId=GA_ACCOUNT_ID,
      webPropertyId=GA_PROPERTY_ID,
      customDataSourceId=GA_DATASET_ID).execute()
  uploads = response["items"]
  cids = [upload["id"] for upload in uploads[1:]]
  delete_request_body = {"customDataImportUids": cids}
  ga_api.management().uploads().deleteUploadData(
      accountId=GA_ACCOUNT_ID,
      webPropertyId=GA_PROPERTY_ID,
      customDataSourceId=GA_DATASET_ID,
      body=delete_request_body).execute()


def write_to_ga_via_mp(df):
  """Write the prediction results into GA via Measurement Protocol.
  Args:
    df: BQML model results dataframe
  """
  pass

    
def main():
  """Code to trigger workflow.
  """
  timestamp_utc = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  try:
    dataframe = read_new_data_from_bq()
    features, dataframe =  preprocess_features(dataframe)
    #df = predict_using_ai_platform(features, dataframe)
    df = predict_model_output(features, dataframe)
    output_df = postprocess_output(df)
    prepare_csv(output_df)
    if GA_IMPORT_METHOD == "di":
      ga_api = authorize_ga_api()
      write_to_ga_via_di(ga_api)
      delete_ga_prev_uploads(ga_api)
    elif GA_IMPORT_METHOD == "mp":
      write_to_ga_via_mp(output_df)
    else:
      raise Exception("GA Import method not found.")
    print("{0},SUCCESS".format(timestamp_utc))
  except Exception as e:
    print("{0},ERROR,{1}".format(timestamp_utc,str(e)))


main()
