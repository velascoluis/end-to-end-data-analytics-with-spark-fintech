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

NOTE: If you want to deploy items one by one, the terraform target list is:
* For LAB 1:
```code
google_project_service.enable_orgpolicy_google_apis
google_project_service.enable_compute_google_apis 
google_project_service.enable_container_google_apis
google_project_service.enable_containerregistry_google_apis 
google_project_service.enable_dataproc_google_apis
google_project_service.enable_bigquery_google_apis 
google_project_service.enable_storage_google_apis
google_project_service.enable_notebooks_google_apis 
google_project_service.enable_aiplatform_google_apis 
google_project_service.enable_logging_google_apis
google_project_service.enable_monitoring_google_apis 
google_project_service.enable_servicenetworking_google_apis
google_project_service.enable_cloudbuild_google_apis 
google_project_service.enable_artifactregistry_google_apis
google_project_service.enable_cloudresourcemanager_google_apis
google_project_service.enable_composer_google_apis 
google_project_service.enable_functions_google_apis 
google_project_service.enable_pubsub_google_apis
google_project_service.enable_dpms_google_apis
google_project_service.enable_cloudrun_admin_google_apis
google_project_service.enable_cloudscheduler_google_apis
module.umsa_creation
module.umsa_role_grants
module.umsa_impersonate_privs_to_admin
module.administrator_role_grants
module.vpc_creation
google_compute_global_address.reserved_ip_for_psa_creation
google_service_networking_connection.private_connection_with_service_networking
google_compute_firewall.allow_intra_snet_ingress_to_any
google_storage_bucket.s8s_spark_bucket_creation
google_storage_bucket.s8s_spark_sphs_bucket_creation
google_storage_bucket.s8s_data_bucket_creation
google_storage_bucket.s8s_code_bucket_creation
null_resource.mnbs_post_startup_bash_creation  
null_resource.data_engineering_notebook_customization
google_storage_bucket_object.scripts_dir_upload_to_gcs
google_bigquery_dataset.bq_dataset_creation
google_bigquery_job.ctas_transactions_creation
google_bigquery_job.ctas_blocks_creation
google_notebooks_runtime.mnb_server_creation
google_artifact_registry_repository.artifact_registry_creation
module.gmsa_role_grants_cc 
google_project_iam_member.grant_editor_default_compute
google_dataproc_cluster.sphs_creation
google_dataproc_metastore_service.datalake_metastore_creation
null_resource.custom_container_image_creation
google_composer_environment.cloud_composer_env_creation 
data google_compute_default_service_account.default 
```



Then, follow instructions for each lab under `end-to-end-data-analytics-with-spark-fintech/<LAB_NAME>/instructions/README.md` 
