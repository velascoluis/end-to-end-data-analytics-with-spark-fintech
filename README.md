# End to end data analytics with SPARK (Fintech edition)

## Introduction

This repository contains two different labs that show four different stages of a data analytics journey:

1. [Data Engineering](01-data-engineering) - Refactor of [s8s-spark-ce-workshop](https://github.com/anagha-google/s8s-spark-ce-workshop)
2. [Streaming](02-streaming)

Most of the user code is a SPARK refactor of BigQuery SQL code featured [here](https://cloud.google.com/blog/products/data-analytics/introducing-six-new-cryptocurrencies-in-bigquery-public-datasets-and-how-to-analyze-them)

## Architecture 

[Architecture and narrative](assets/end_to_end_data_analytics_with_SPARK.pdf)

## Installation

The deployment is fully terraformed. For each lab and from a [Google Cloud Cloud Shell](https://cloud.google.com/shell) terminal logged as your admin user, execute the following commands:

On the top of the Google Cloud console, ensure an existing project is selected. Then run the following commands:

```console
REGION=us-central1 # Change as needed
ZONE=us-central1-a # change as needed
```


```console
~$ cd <LAB_NAME>
# e.g. where <LAB_NAME> is 01-data-engineering, 02-sreaming
~$ ./local_project_launcher.sh ${GOOGLE_CLOUD_PROJECT} ${REGION} ${ZONE} ${USER_EMAIL}
```

For example:

```console
~$ source local_project_launcher.sh ${GOOGLE_CLOUD_PROJECT} ${REGION} ${ZONE} ${USER_EMAIL}
```

Then, follow instructions for each lab under `<LAB_NAME>/instructions/en.md` 





