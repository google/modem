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


# ------------------------------------------------------------------

# GA Details
GA_ACCOUNT_ID = ""   # requierd for DI only
GA_PROPERTY_ID = ""   # required for both DI and MP
GA_DATASET_ID = ""   # required for DI only
GA_IMPORT_METHOD = "di"   # "di" - Data Import or "mp" - Measurement Protocol

# GA measurement protocol hit details. Add any additional fields which are
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


# BigQuery Query Details - BQML query or normal BQ Query possible
# Ensure that the BQ result headers resemble the data import schema in SELECT
# E.g. If data import schema looks like  - ga:dimension32, ga:dimension1, etc.
# BQ result headers should like SELECT X AS ga_dimension32, Y AS ga_dimension1
BQML_PREDICT_QUERY = """
                     """

# -------------------------------------------------------------------

# Options for logging & error monitoring
# LOGGING: Create BQ Table for logs with schema as follows -
# time TIMESTAMP, status STRING, error ERROR
ENABLE_BQ_LOGGING = False
# ERROR MONITORING: Sign up for the free Sendgrid API.
ENABLE_SENDGRID_EMAIL_REPORTING = False


# (OPTIONAL) Workflow Logging - BQ details, if enabled
GCP_PROJECT_ID = ""
BQ_DATASET_NAME = ""
BQ_TABLE_NAME = ""


# (OPTIONAL) Email Reporting - Sendgrid details, if enabled
SENDGRID_API_KEY = ""
TO_EMAIL = ""

# -------------------------------------------------------------------

# (OPTIONAL) Email Reporting - Additional Parameters
FROM_EMAIL = "workflow@example.com"
SUBJECT = "FAILED: Audience Upload to GA"
HTML_CONTENT = """
               <p>
               Hi WorkflowUser, <br>
               Your BQML Custom Audience Upload has failed- <br>
               Time: {0} UTC <br>
               Reason: {1}
               </p>
               """
