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

#........................................................................
# Purpose: Create SPARK Serverless session
#........................................................................



GCLOUD_BIN=`which gcloud`



ERROR_EXIT=1



PROJECT_ID="${GCLOUD_BIN}"=`"${GCLOUD_BIN}" config list --format "value(core.project)" 2>/dev/null`
REGION=`"${GCLOUD_BIN}" compute project-info describe --project ${PROJECT_ID} --format "value(commonInstanceMetadata.google-compute-default-region)" 2>/dev/null`



if [ ! "${CLOUD_SHELL}" = true ]; then
    echo "This script needs to run on Google Cloud Shell. Exiting ..."
    exit ${ERROR_EXIT}
fi


"${GCLOUD_BIN}" beta dataproc sessions create spark sparkhflab01-${RANDOM} --project=${PROJECT_ID} --location=REGION --container-image=gcr.io/s8s-spark-${PROJECT_ID}/customer_churn_image:1.0.0 --history-server-cluster=projects/${PROJECT_ID}/regions/REGION/clusters/s8s-sphs-${PROJECT_ID} --metastore-service=projects/${PROJECT_ID}/locations/REGION/services/s8s-dpms-${PROJECT_ID} --property=spark.jars.packages=com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.25.2 --service-account=s8s-lab-sa@${PROJECT_ID}.iam.gserviceaccount.com --subnet=spark-snet


echo "###########################################################################################"
echo "${LOG_DATE} Execution finished! ..."



