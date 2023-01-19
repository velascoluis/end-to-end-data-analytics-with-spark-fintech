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
# Purpose: Upload DAG files to the Composer bucket
#........................................................................

GCLOUD_BIN=`which gcloud`
GSUTIL_BIN=`which gsutil`

LOG_DATE=`date`
echo "###########################################################################################"
echo "${LOG_DATE}  SPARK Hackfest - upload DAG  .."

if [ ! "${CLOUD_SHELL}" = true ] ; then
    echo "This script needs to run on Google Cloud Shell. Exiting ..."
    exit 1
fi

PROJECT_ID=`"${GCLOUD_BIN}" config list --format "value(core.project)" 2>/dev/null`
echo "PROJECT_ID : ${PROJECT_ID}"


"${GSUTIL_BIN}" cp data_eng_dag_step_*.py "gs://s8s_code_bucket-"${PROJECT_ID}"/dataeng/"

DAG_FOLDER=`${GSUTIL_BIN} ls gs://* | grep dags`
"${GSUTIL_BIN}" cp data_eng_pipeline.py ${DAG_FOLDER}

LOG_DATE=`date`
echo "###########################################################################################"
echo "${LOG_DATE} Execution finished! ..."




