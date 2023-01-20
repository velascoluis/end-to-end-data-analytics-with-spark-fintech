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

KAFKA_TOPIC="transactions"
PROJECT_ID=${GOOGLE_CLOUD_PROJECT}
BQ_SCRATCH_BUCKET="s8s-spark-bucket-${PROJECT_ID}/scratcha"
CHECKPOINT_BUCKET_URI="s8s-spark-bucket-${PROJECT_ID}/checkpoint"
BQ_TABLE="crypto_bitcoin.entries"
KAFKA_CONNECTOR_JAR_GCS_URI="gs://s8s_code_bucket-${PROJECT_ID}/spark-sql-kafka-0-10_2.12-3.2.1.jar"
BQ_CONNECTOR_JAR_GCS_URI="gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.27.1.jar"
SERVICE_ACCOUNT=s8s-lab-sa@${PROJECT_ID}.iam.gserviceaccount.com
KAFKA_PACKAGE_COORDS="org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1"
SPARK_PACKAGE_COORDS="com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.22.2,${KAFKA_PACKAGE_COORDS}"

gcloud dataproc batches submit pyspark structured_streaming.py --async --region=us-central1 --properties "spark.dynamicAllocation.enabled=false,spark.jars.packages=${KAFKA_PACKAGE_COORDS}" --deps-bucket=s8s-spark-bucket-${GOOGLE_CLOUD_PROJECT} --jars=${BQ_CONNECTOR_JAR_GCS_URI},${KAFKA_CONNECTOR_JAR_GCS_URI} --subnet=spark-snet  --service-account=${SERVICE_ACCOUNT} -- ${KAFKA_TOPIC} ${PROJECT_ID} ${BQ_SCRATCH_BUCKET} ${CHECKPOINT_BUCKET_URI} ${BQ_TABLE} true