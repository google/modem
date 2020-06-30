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

"""Specifying the correct parameters."""

# ------------------------------------------------------------------

# GA Details

GA_ACCOUNT_ID = ""
GA_PROPERTY_ID = ""
GA_DATASET_ID = ""
GA_IMPORT_METHOD = "di"  # "di" - Data Import or "mp" - Measurement Protocol

# -------------------------------------------------------------------
# BigQuery Dataset and Table for GA Data - GA_BQ_DATASET_NAME, GA_BQ_TABLE_NAME
# MODEL_INPUT_COL_NAMES expects a list of column names used for prediction.
#
# E.g. If your BigQuery table has following schema ->
# clientId, clientName, feature1, feature2, feature3
# and you are using feature1, feature2, feature3 as model inputs, then
# MODEL_INPUT_COL_NAMES = ['feature1', 'feature2', 'feature3']
#
# CSV_COLUMN_MAP is a dictionary that maps BigQuery column names to
# corresponding Data Import schema headers.
# To ensure that the Data Import CSV is correctly created,
# you need to provide the CSV_COLUMN_MAP.
# E.g., If your BigQuery table has following schema ->
# clientId, clientName, feature1, feature2, feature3,
# and you'd like to export clientId, clientName and model output via Data Import
# with a CSV schema of 'ga:userId', 'ga:dimension1', 'ga:dimension2',
# your CSV_COLUMN_MAP will look as follows-
# (predicted is always reserved for model output)
# CSV_COLUMN_MAP = {'clientId' : 'ga:userId',
#                   'clientName': 'ga:dimension1',
#                   'predicted' : 'ga:dimension2'}

GCP_PROJECT = ""
GA_BQ_DATASET_NAME = ""
GA_BQ_TABLE_NAME = ""

MODEL_INPUT_COL_NAMES = []

COLUMN_MAP = {"predicted": ""}

# -------------------------------------------------------------------
# AI Platform Details

AI_PLATFORM_MODEL_NAME = ""
AI_PLATFORM_VERSION_NAME = ""
