# End to end data analytics with SPARK (Fintech edition)

## Introduction

This repository contains two different labs that show four different stages of a data analytics journey:

1. [Data Engineering](01-data-engineering) - Refactor of [s8s-spark-ce-workshop](https://github.com/anagha-google/s8s-spark-ce-workshop)
2. [Streaming](02-streaming)

Most of the user code is a SPARK refactor of BigQuery SQL code featured [here](https://cloud.google.com/blog/products/data-analytics/introducing-six-new-cryptocurrencies-in-bigquery-public-datasets-and-how-to-analyze-them)

## Architecture 

[Architecture and narrative](assets/end_to_end_data_analytics_with_SPARK.pdf)

## Installation

The deployment is fully terraformed.
From a [Google Cloud Cloud Shell](https://cloud.google.com/shell) terminal logged as your admin user, execute the following commands:
1. Ensure a existing project is selected, you can check with:

```console
~$ env | grep GOOGLE 
# e.g. make sure the ENV variable GOOGLE_CLOUD_PROJECT is setup.
```

2. Clone this repository:

```console
~$ git clone https://github.com/velascoluis/end-to-end-data-analytics-with-spark-fintech.git
```

3. Setup variables:

```console
~$  REGION=<GCP_REGION> 
~$  ZONE=<GZP_ZONE>
# e.g. where <GCP_REGION> and <GZP_ZONE> are valid GCP zones
```
3. Launch the terraform script to deploy the lab infraestructure:

```console
~$ cd end-to-end-data-analytics-with-spark-fintech/<LAB_NAME>/terraform
# e.g. where <LAB_NAME> is 01-data-engineering, 02-sreaming
~$ ./local_project_launcher.sh ${GOOGLE_CLOUD_PROJECT} ${REGION} ${ZONE} ${USER_EMAIL} all
```

For example:

```console
env | grep GOOGLE
REGION=us-central1
ZONE=us-central1-a
git clone https://github.com/velascoluis/end-to-end-data-analytics-with-spark-fintech.git
cd end-to-end-data-analytics-with-spark-fintech/01-data-engineering/terraform
source local_project_launcher.sh ${GOOGLE_CLOUD_PROJECT} ${REGION} ${ZONE} ${USER_EMAIL} all
```

Then, follow instructions for each lab under `end-to-end-data-analytics-with-spark-fintech/<LAB_NAME>/instructions/README.md` 
