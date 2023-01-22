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


PYTHON_BIN=`which python3`
PIP_BIN=`which pip3`


LOG_DATE=`date`
echo "###########################################################################################"
echo "${LOG_DATE}  SPARK Hackfest - launch streamlit   .."


if [ ! "${CLOUD_SHELL}" = true ] ; then
    echo "This script needs to run on Google Cloud Shell. Exiting ..."
    exit 1
fi

export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
${PYTHON_BIN} -m venv local_test_env
source local_test_env/bin/activate
${PIP_BIN} install -r requirements.txt
streamlit run transactions_dashboard.py --server.port=8080 --server.enableCORS=false --server.enableXsrfProtection=false