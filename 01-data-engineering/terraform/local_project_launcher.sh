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
# Purpose: Test lab on a local non Qwiklabs project 
#........................................................................

TERRAFORM_BIN=`which terraform`

ERROR_EXIT=1
if [ ! "${CLOUD_SHELL}" = true ]; then
    echo "This script needs to run on Google Cloud Shell. Exiting ..."
    exit ${ERROR_EXIT}
fi

if [ "${#}" -ne 5 ]; then
    echo "Illegal number of parameters. Exiting ..."
    echo "Usage: ${0} <gcp_project_id> <gcp_region> <gcp_zone> <gcp_user_id> <all|target_resource> " 
    echo "Exiting ..."
     exit ${ERROR_EXIT}
fi


GCP_PROJECT_ID=${1}
GCP_REGION=${2}
GCP_ZONE=${3}
GCP_USER_ID=${4}
TARGET=${5}

LOG_DATE=`date`
echo "###########################################################################################"
echo "${LOG_DATE} Launching Terraform ..."


"${TERRAFORM_BIN}" init -reconfigure
if [ ! "${?}" -eq 0 ]; then
        LOG_DATE=`date`
        echo "${LOG_DATE} Unable to run ${TERRAFORM_BIN} init -reconfigure. Exiting ..."
        exit 1
fi
"${TERRAFORM_BIN}" validate
if [ ! "${?}" -eq 0 ]; then
        LOG_DATE=`date`
        echo "${LOG_DATE} Unable to run ${TERRAFORM_BIN} validate. Exiting ..."
        exit 1
fi

"${TERRAFORM_BIN}" plan \
    -var="gcp_project_id=${GCP_PROJECT_ID}" \
    -var="gcp_region=${GCP_REGION}" \
    -var="gcp_zone=${GCP_ZONE}" \
    -var="gcp_user_id=${GCP_USER_ID}" 
if [ ! "${?}" -eq 0 ]; then
    LOG_DATE=`date`
    echo "${LOG_DATE} Unable to run ${TERRAFORM_BIN} plan. Exiting ..."
    exit 1
fi

if [  "${TARGET}" = "all" ]; then
    "${TERRAFORM_BIN}" apply \
    -var="gcp_project_id=${GCP_PROJECT_ID}" \
    -var="gcp_region=${GCP_REGION}" \
    -var="gcp_zone=${GCP_ZONE}" \
    -var="gcp_user_id=${GCP_USER_ID}" \
    --auto-approve 
    if [ ! "${?}" -eq 0 ]; then
        LOG_DATE=`date`
        echo "${LOG_DATE} Unable to run ${TERRAFORM_BIN} apply. Exiting ..."
        exit 1
    fi  
else
    "${TERRAFORM_BIN}" apply 
    -var="gcp_project_id=${GCP_PROJECT_ID}" \
    -var="gcp_region=${GCP_REGION}" \
    -var="gcp_zone=${GCP_ZONE}" \
    -var="gcp_user_id=${GCP_USER_ID}" \
    --target="${TARGET}" 
    --auto-approve \
    if [ ! "${?}" -eq 0 ]; then
        LOG_DATE=`date`
        echo "${LOG_DATE} Unable to run ${TERRAFORM_BIN} apply. Exiting ..."
        exit 1
    fi  

fi

 
LOG_DATE=`date`
echo "###########################################################################################"
echo "${LOG_DATE} Execution finished! ..."

