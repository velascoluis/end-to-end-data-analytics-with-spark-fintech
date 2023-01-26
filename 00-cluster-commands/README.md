# Dataproc cluster commands for common tasks and examples 

## Set bash variables
```
ACCOUNT=$(gcloud config get account --quiet)
PROJECT=$(gcloud config get project --quiet)
REGION=region-value-here
ZONE=zone-value-here
CLUSTER=cluster-name-here
```

## Spark job with custom properties
```
gcloud dataproc jobs submit spark \
  --cluster=$CLUSTER \
  --region=$REGION \
  --jar=my_jar.jar \
  --properties='spark.executor.cores=5,spark.executor.memory=4608mb' \
  -- arg1 arg2
```

## Create Auto Scaling Cluster

```
#create a auto scaling policy yaml file, save it as auto.yaml
workerConfig:
  minInstances: 10
  maxInstances: 10
  weight: 1
secondaryWorkerConfig:
  minInstances: 0
  maxInstances: 100
  weight: 1
basicAlgorithm:
  cooldownPeriod: 2m
  yarnConfig:
    scaleUpFactor: 0.05
    scaleDownFactor: 1.0
    scaleUpMinWorkerFraction: 0.0
    scaleDownMinWorkerFraction: 0.0
    gracefulDecommissionTimeout: 1h

#create a new policy from this file
gcloud dataproc autoscaling-policies import my-auto-scaling-100-secondary-workers \
    --source=auto.yaml \
    --region=$REGION

#test creating a cluster with this policy 
gcloud dataproc clusters create my-auto-scaling-cluster \
    --enable-component-gateway \
    --autoscaling-policy=my-auto-scaling-100-secondary-workers \
    --project=$PROJECT \
    --region=$REGION
    
#run a small job 
gcloud dataproc jobs submit pyspark \
file:///usr/lib/spark/examples/src/main/python/pi.py \
--project=$PROJECT \
--region=$REGION \
--cluster=my-auto-scaling-cluster


#run a big job
gcloud dataproc jobs submit pyspark \
file:///usr/lib/spark/examples/src/main/python/pi.py \
--project=$PROJECT \
--region=$REGION \
--cluster=my-auto-scaling-cluster -- 10000

```

## Create Custom Constraints (Fleet management)
### Force enable component gateway for all clusters 

```
#yaml file for constraint, save as custom.yaml
name: organizations/ORGANIZATION_ID/customConstraints/custom.dataprocEnableComponentGateway
resourceTypes:
- dataproc.googleapis.com/Cluster
methodTypes:
    - CREATE
    - UPDATE
condition: resource.config.endpointConfig.enableHttpPortAccess==true
actionType: ALLOW
displayName: "Enforce enabling Dataproc Component Gateway"
description: "Only allow Dataproc cluster creation if the Component Gateway is enabled"

#add this as a custom constraint
gcloud org-policies set-custom-constraint /home/user/custom.yaml

#list constraints
gcloud org-policies list-custom-constraints --organization=<org-id>

#create policy json file to enable this constraint, save as custom-enable.json
      name: projects/PROJECT_ID/policies/custom.dataprocEnableComponentGateway
      spec:
        rules:
        - enforce: true
   
gcloud org-policies set-policy  /home/user/custom-enable.json

#test a cluster creation for success or failure. 
gcloud dataproc clusters create test-failure-cluster \
    --region=$REGION \ 
    --project=$PROJECT

#test success
gcloud dataproc clusters create test-failure-cluster \
    --enable-component-gateway \
    --region=$REGION \ 
    --project=$PROJECT
```

## PySpark with BQ Connector

```
gcloud dataproc jobs submit pyspark --region $REGION \
--cluster $CLUSTER \
--jars gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.25.2.jar  \
<your-python-file>.py 
```

## Serverless Spark
### Batches

```
OUTPUT_BUCKET=your-bucket-here
PHS_CLUSTER=your-cluster-here

gcloud storage buckets create --project=$PROJECT gs://$OUTPUT_BUCKET


Spark Serverless
------------------

gcloud beta dataproc batches submit spark \
--project=$PROJECT \
--region=$REGION \
--jars=file:///usr/lib/spark/examples/jars/spark-examples.jar \
--class=org.apache.spark.examples.SparkPi \
-- 20000

10 gb shuffle
----------------

gcloud beta dataproc batches submit spark \
--project=$PROJECT \
--region=$REGION \
--jar=gs://dataproc-spark-preview/bigshuffle.jar \
-- shuffle \
-i gs://dataproc-datasets-us-central1/teragen/100tb/ascii_sort_1GB_input.000000* \
-o gs://$OUTPUT_BUCKET \
--output-partitions 20 \
-v

100 gb shuffle
----------------

gcloud beta dataproc batches submit spark \
--project=$PROJECT \
--region=$REGION \
--jar=gs://dataproc-spark-preview/bigshuffle.jar \
-- shuffle \
-i gs://dataproc-datasets-us-central1/teragen/100tb/ascii_sort_1GB_input.00000* \
-o gs://$OUTPUT_BUCKET \
--output-partitions 20 \
-v

100 gb shuffle with PHS
------------------------

gcloud beta dataproc batches submit spark \
--project=$PROJECT \
--region=$REGION \
--history-server-cluster=projects/$PROJECT/regions/$REGION/clusters/$PHS_CLUSTER \
--jar=gs://dataproc-spark-preview/bigshuffle.jar \
-- shuffle \
-i gs://dataproc-datasets-us-central1/teragen/100tb/ascii_sort_1GB_input.00000* \
-o gs://$OUTPUT_BUCKET \
--output-partitions 20 \
-v

100 gb shuffle with PHS & Set number of Executors 
---------------------------------------------------

gcloud beta dataproc batches submit spark \
--project=$PROJECT \
--region=$REGION \
--history-server-cluster=projects/$PROJECT/regions/$REGION/clusters/$PHS_CLUSTER \
--properties='spark.executor.instances=25' \
--jar=gs://dataproc-spark-preview/bigshuffle.jar \
-- shuffle \
-i gs://dataproc-datasets-us-central1/teragen/100tb/ascii_sort_1GB_input.00000* \
-o gs://$OUTPUT_BUCKET \
--output-partitions 20 \
-v
```
