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

cron_schedule="* * * * *"
echo "$cron_schedule cd ~/modem/pythonML/pipeline && python main.py >> workflow.csv" | crontab -
echo "Your workflow has been schedule with the cron schedule of $cron_schedule. Enjoy!" 
