# Dataproc cluster commands for common tasks and examples 

## Set bash variables
```
ACCOUNT=$(gcloud config get account --quiet)
PROJECT=$(gcloud config get project --quiet)
REGION=region-value-here
ZONE=zone-value-here
CLUSTER=cluster-name-here
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


## PySpark with BQ Connector

```
gcloud dataproc jobs submit pyspark --region $REGION \
--cluster $CLUSTER \
--jars gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.25.2.jar  \
<your-python-file>.py 
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



