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

exists_rule=$(gcloud compute firewall-rules list | grep "default-allow-ssh" | wc -l)
if [ $exists_rule -eq 0 ] 
then 
  gcloud compute firewall-rules create default-allow-ssh --allow tcp:22;
  echo "New firewall rule created."
else
  echo "The correct firewall rules exist." 
fi
