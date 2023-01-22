# ======================================================================================
# ABOUT
# This airflow DAG orchestrates data engineering
# ======================================================================================

import os
from airflow.models import Variable
from datetime import datetime
from airflow import models
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateBatchOperator, DataprocGetBatchOperator)
from datetime import datetime
from airflow.utils.dates import days_ago
import string
import random

# .......................................................
# Variables
# .......................................................

# {{
# a) General
randomizerCharLength = 10
randomVal = ''.join(random.choices(string.digits, k=randomizerCharLength))
airflowDAGName = "mining-pool-class-data-eng"
batchIDPrefix = f"{airflowDAGName}-edo-{randomVal}"
# +
# b) Capture from Airflow variables
region = models.Variable.get("region")
subnet = models.Variable.get("subnet")
phsServer = Variable.get("phs_server")
containerImageUri = Variable.get("container_image_uri")
bqDataset = Variable.get("bq_dataset")
umsaFQN = Variable.get("umsa_fqn")
bqConnectorJarUri = Variable.get("bq_connector_jar_uri")
# +
# c) For the Spark application
pipelineID = randomVal
projectID = models.Variable.get("project_id")
projectNbr = models.Variable.get("project_nbr")
displayPrintStatements = Variable.get("display_print_statements")
# +
# d) Arguments array
batchScoringArguments = [f"--pipelineID={pipelineID}",
                         f"--projectID={projectID}",
                         f"--projectNbr={projectNbr}",
                         f"--displayPrintStatements={displayPrintStatements}"]
# +
# e) PySpark script to execute
dataEngStep1 = "gs://s8s_code_bucket-" + \
    projectNbr+"/dataeng/data_eng_dag_step_1.py"
dataEngStep2 = "gs://s8s_code_bucket-" + \
    projectNbr+"/dataeng/data_eng_dag_step_2.py"
# }}

# .......................................................
# s8s Spark batch config
# .......................................................

s8sSparkBatchConfigStep1 = {
    "pyspark_batch": {
        "main_python_file_uri": dataEngStep1,
        "args": batchScoringArguments,
        "jar_file_uris": [bqConnectorJarUri]
    },
    "runtime_config": {
        "container_image": containerImageUri
    },
    "environment_config": {
        "execution_config": {
            "service_account": umsaFQN,
            "subnetwork_uri": subnet
        },
        "peripherals_config": {
            "spark_history_server_config": {
                "dataproc_cluster": f"projects/{projectID}/regions/{region}/clusters/{phsServer}"
            }
        }
    }
}

s8sSparkBatchConfigStep2 = {
    "pyspark_batch": {
        "main_python_file_uri": dataEngStep2,
        "args": batchScoringArguments,
        "jar_file_uris": [bqConnectorJarUri]
    },
    "runtime_config": {
        "container_image": containerImageUri
    },
    "environment_config": {
        "execution_config": {
            "service_account": umsaFQN,
            "subnetwork_uri": subnet
        },
        "peripherals_config": {
            "spark_history_server_config": {
                "dataproc_cluster": f"projects/{projectID}/regions/{region}/clusters/{phsServer}"
            }
        }
    }
}



# .......................................................
# DAG
# .......................................................

with models.DAG(
    airflowDAGName,
    schedule_interval=None,
    start_date=days_ago(2),
    catchup=False,
) as scoringDAG:
    miningPoolDataEngStep1 = DataprocCreateBatchOperator(
        task_id="Mining-Pool-Class-Data-Eng-Step1",
        project_id=projectID,
        region=region,
        batch=s8sSparkBatchConfigStep1,
        batch_id=f"{batchIDPrefix}-step-1"
    )

    miningPoolDataEngStep2 = DataprocCreateBatchOperator(
        task_id="Mining-Pool-Class-Data-Eng-Step2",
        project_id=projectID,
        region=region,
        batch=s8sSparkBatchConfigStep2,
        batch_id=f"{batchIDPrefix}-step-2"
    )

    miningPoolDataEngStep1 >> miningPoolDataEngStep2




    