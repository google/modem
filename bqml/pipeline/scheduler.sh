#!/bin/bash

###########################################################################
#
#  Copyright 2020 Google Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################
#
# Instructions -
# 1. Edit the following params in the Cloud Functions UI. Don't insert spaces between param and value.
#    a. JOBNAME: Any name you like, e.g. "schedule_model_upload"
#    b. SCHEDULE: Specify the schedule in a cron-tab format e.g. "45 23 * * *" to run job every day at 11:45 pm
#    c. TIMEZONE: Specify timezone e.g. "EST", "PST", "CST" etc. for US time zones
#    d. FUNCTION_URL: The URL can be found within the 'Cloud Function > Trigger' It has the format "https://<PROJECT_ID>.cloudfunctions.net/<FUNCTION_NAME>"
#    e. SERVICE_ACCOUNT_EMAIL: App Engine Default service account email of the form "<PROJECT_ID>@appspot.gserviceaccount.com"


JOB_NAME=""
SCHEDULE=""
TIMEZONE=""
FUNCTION_URL=""
SERVICE_ACCOUNT_EMAIL=""
gcloud scheduler jobs create http $JOB_NAME  --schedule="$SCHEDULE" --uri=$FUNCTION_URL --time-zone=$TIMEZONE --oidc-service-account-email=$SERVICE_ACCOUNT_EMAIL --attempt-deadline="540s"

