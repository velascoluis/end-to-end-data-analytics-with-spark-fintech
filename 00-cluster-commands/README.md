#Dataproc cluster commands for common tasks and examples 

##Set bash variables
```
ACCOUNT=$(gcloud config get account --quiet)
PROJECT=$(gcloud config get project --quiet)
REGION=region-value-here
ZONE=zone-value-here
CLUSTER=cluster-name-here
```


##PySpark with BQ Connector

```
gcloud dataproc jobs submit pyspark --region $REGION \
--cluster $CLUSTER \
--jars gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.25.2.jar  \
<your-python-file>.py 
```





