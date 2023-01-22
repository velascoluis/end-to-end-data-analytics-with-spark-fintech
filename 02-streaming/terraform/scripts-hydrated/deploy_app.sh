#!/bin/sh
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

GCLOUD_BIN=`which gcloud`


LOG_DATE=`date`
echo "###########################################################################################"
echo "${LOG_DATE}  SPARK Hackfest - launch streamlit docker build   .."


if [ ! "${CLOUD_SHELL}" = true ] ; then
    echo "This script needs to run on Google Cloud Shell. Exiting ..."
    exit 1
fi

PROJECT_ID=`"${GCLOUD_BIN}" config list --format "value(core.project)" 2>/dev/null`
SERVICE_NAME='transactions-dashboard'
IMAGE_NAME='transactions-dashboard'
GCP_REGION='us-central1'


echo "Deploying image ..."

"${GCLOUD_BIN}" run deploy ${SERVICE_NAME} --source . --platform managed --region ${GCP_REGION}