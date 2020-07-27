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

"""Pipeline code for PythonML activation to GA."""

import datetime
import warnings
from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
import httplib2
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import params
import pandas as pd
from google.cloud import bigquery
import pkl_predictions  


GA_ACCOUNT_ID = params.GA_ACCOUNT_ID
GA_PROPERTY_ID = params.GA_PROPERTY_ID
GA_DATASET_ID = params.GA_DATASET_ID
GA_IMPORT_METHOD = params.GA_IMPORT_METHOD
BQ_READ_QUERY = params.BQ_READ_QUERY
MODEL_FILE_NAME = params.MODEL_FILE_NAME

SERVICE_ACCOUNT_FILE = "svc_key.json"
CLOUD_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
CSV_LOCATION = "output.csv"
GA_SCOPES = [
    "https://www.googleapis.com/auth/analytics.readonly",
    "https://www.googleapis.com/auth/analytics.edit",
    "https://www.googleapis.com/auth/analytics"
]
GA_API_NAME = "analytics"
GA_API_VERSION = "v3"

warnings.simplefilter(action="ignore", category=FutureWarning)


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


def read_from_bq():
  """Reads the prediction query from Bigquery using BQML.

  Returns:
    dataframe: BQML model results dataframe.
  """
  credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/cloud-platform"])
  bq_client = bigquery.Client(credentials=credentials, project=credentials.project_id)
  #bq_client = bigquery.Client()
  query_job = bq_client.query(BQ_READ_QUERY)
  results = query_job.result()
  dataframe = results.to_dataframe()
  return dataframe


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


def main():
  """Code to trigger workflow.
  """
  timestamp_utc = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  try:
    dataframe = read_from_bq()
    print("Read the input data from BQ.")
    processed_df = pkl_predictions.preprocess(dataframe)
    print("Pre-processed the input data.")
    results_df = pkl_predictions.get_predictions(MODEL_FILE_NAME,
                                                 processed_df)
    print("Fetched prediction results.")
    if GA_IMPORT_METHOD == "di":
      print("Uploading to GA via DI.....")
      prepare_csv(results_df)
      ga_api = authorize_ga_api()
      write_to_ga_via_di(ga_api)
      delete_ga_prev_uploads(ga_api)
      print("Upload via DI complete.")
    elif GA_IMPORT_METHOD == "mp":
      write_to_ga_via_mp(output_df)
    else:
      raise Exception("GA Import method not found.")
    print("{0},SUCCESS".format(timestamp_utc))
  except Exception as e:
    print("{0},ERROR,{1}".format(timestamp_utc, str(e)))


main()
