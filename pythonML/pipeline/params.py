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

MODEL_FILE_NAME = "model.pkl"

# BigQuery Query Details - BQML query or normal BQ Query possible
# Ensure that the BQ result headers resemble the data import schema in SELECT
# E.g. If data import schema looks like  - ga:dimension32, ga:dimension1, etc.
# BQ result headers should like SELECT X AS ga_dimension32, Y AS ga_dimension1
BQ_READ_QUERY = """
                """

# GA Details
GA_IMPORT_METHOD = "di"   # "di" - Data Import or "mp" - Measurement Protocol


GA_ACCOUNT_ID = ""   # required for DI only
GA_PROPERTY_ID = ""   # required for both DI and MP
GA_DATASET_ID = ""   # required for DI only


# Only needed if using GA measurement protocol. 
# Add any additional fields which are
# the same for all hits here.
GA_MP_STANDARD_HIT_DETAILS = {
    # mandatory fields below. Do not remove.
    "v": 1, # MP API version
    "tid": GA_PROPERTY_ID,  # ga property id - same as above
    "t": "",  #  hit type
    # optional fields below:
    "ni": 1,   # non interaction hit: 1 or 0,
    "ec": "",  # event category
    "ea": "",  #  event action
    "el": "",  # event label
    "ds": "",  # data source
    "ua": "modem",  # user agent override
}
