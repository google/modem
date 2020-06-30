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

echo "~~~~~~~~ Welcome ~~~~~~~~~~"
echo "Thanks for using BQML modem deployment." 
echo "---------------------------"
read -p "Please enter your GCP PROJECT ID: " project_id
echo "---------------------------"
read -p "Please enter your desired FUNCTION NAME: " function_name
echo "---------------------------"
echo "~~~~~~~~ Creating function ~~~~~~~~~~"
svc_account_email=`gcloud iam service-accounts list --filter="App Engine default service account" | awk 'FNR == 2{print $6}'` 
sed_expr='s/SERVICE_ACCOUNT_EMAIL=""/SERVICE_ACCOUNT_EMAIL="'$svc_account_email'"/'
sed -i $sed_expr scheduler.sh
gcloud functions deploy $function_name --project $project_id --runtime python37 --memory 2GB --timeout 540s --trigger-http --entry-point trigger_workflow
