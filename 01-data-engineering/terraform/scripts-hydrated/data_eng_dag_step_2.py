# ............................................................
# Preprocessing - Step 2
# ............................................................
# This script performs data preprocessing (step 2) from intermediate data in BigQuery
# and persists to BigQuery
# ............................................................

import sys,logging,argparse
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from datetime import datetime



def fnParseArguments():
# {{ Start 
    """
    Purpose:
        Parse arguments received by script
    Returns:
        args
    """
    argsParser = argparse.ArgumentParser()
    argsParser.add_argument(
        '--pipelineID',
        help='Unique ID for the pipeline stages for traceability',
        type=str,
        required=True)
    argsParser.add_argument(
        '--projectNbr',
        help='The project number',
        type=str,
        required=True)
    argsParser.add_argument(
        '--projectID',
        help='The project id',
        type=str,
        required=True)
    argsParser.add_argument(
        '--displayPrintStatements',
        help='Boolean - print to screen or not',
        type=bool,
        required=True)
    return argsParser.parse_args()
# }} End fnParseArguments()

def fnMain(logger, args):
# {{ Start main

    # 1. Capture Spark application input
    pipelineID = args.pipelineID
    projectNbr = args.projectNbr
    projectID = args.projectID
    displayPrintStatements = args.displayPrintStatements

    # 1b. Variables 
    bqDatasetNm = f"{projectID}.customer_churn_ds"
    appBaseName = "customer-churn-model"
    appNameSuffix = "preprocessing"
    appName = f"{appBaseName}-{appNameSuffix}"
    scratchBucketUri = f"s8s-spark-bucket-{projectNbr}/{appBaseName}/pipelineId-{pipelineID}/{appNameSuffix}"
    miners_table = f"{bqDatasetNm}.miners"
    minig_pool_class_df_output_ages_table = f"{bqDatasetNm}.minig_pool_class_df_output_ages"
    minig_pool_class_df_input_ages_table = f"{bqDatasetNm}.minig_pool_class_df_input_ages"
    minig_pool_class_df_output_monthly_stats_table = f"{bqDatasetNm}.minig_pool_class_df_output_monthly_stats"
    minig_pool_class_df_input_monthly_stats_table = f"{bqDatasetNm}.minig_pool_class_df_input_monthly_stats"
    output_idle_times_table = f"{bqDatasetNm}.output_idle_times"
    input_idle_times_table = f"{bqDatasetNm}.input_idle_times"
    minig_pool_class_table = f"{bqDatasetNm}.minig_pool_class"

    pipelineExecutionDt = datetime.now().strftime("%Y%m%d%H%M%S")

    # 1c. Display input and output
    if displayPrintStatements:
        logger.info("Starting STEP 2 data preprocessing for the *Mining Pool Classifier* pipeline")
        logger.info(".....................................................")
        logger.info(f"The datetime now is - {pipelineExecutionDt}")
        logger.info(" ")
        logger.info("INPUT PARAMETERS-")
        logger.info(f"....pipelineID={pipelineID}")
        logger.info(f"....projectID={projectID}")
        logger.info(f"....projectNbr={projectNbr}")
        logger.info(f"....displayPrintStatements={displayPrintStatements}")
        logger.info(" ")
        logger.info("EXPECTED SETUP-")  
        logger.info(f"....BQ Dataset={bqDatasetNm}")
       
    try:
       
        logger.info('....Initializing spark & spark configs')
        spark = SparkSession.builder.appName(appName).getOrCreate()

        
        spark.conf.set("parentProject", projectID)
        spark.conf.set("temporaryGcsBucket", scratchBucketUri)

        
        logger.info('....Read source data')

        miners = spark.read.format('bigquery').option('table', miners_table).load()

        minig_pool_class_df_output_ages = spark.read.format('bigquery').option('table', minig_pool_class_df_output_ages_table).load()
        minig_pool_class_df_input_ages = spark.read.format('bigquery').option('table', minig_pool_class_df_input_ages_table).load()
        minig_pool_class_df_output_monthly_stats = spark.read.format('bigquery').option('table', minig_pool_class_df_output_monthly_stats_table).load()
        minig_pool_class_df_input_monthly_stats = spark.read.format('bigquery').option('table', minig_pool_class_df_input_monthly_stats_table).load()
        output_idle_times = spark.read.format('bigquery').option('table', output_idle_times_table).load()
        input_idle_times = spark.read.format('bigquery').option('table', input_idle_times_table).load()
          




       
        
        miners_join = minig_pool_class_df_output_ages.join(minig_pool_class_df_output_monthly_stats, minig_pool_class_df_output_ages.output_ages_address == minig_pool_class_df_output_monthly_stats.output_monthly_stats_address) \
            .join(output_idle_times, minig_pool_class_df_output_ages.output_ages_address == output_idle_times.idle_time_address) \
            .join(minig_pool_class_df_input_monthly_stats, minig_pool_class_df_output_ages.output_ages_address == minig_pool_class_df_input_monthly_stats.input_monthly_stats_address) \
            .join(minig_pool_class_df_input_ages, minig_pool_class_df_output_ages.output_ages_address == minig_pool_class_df_input_ages.input_ages_address) \
            .join(input_idle_times, minig_pool_class_df_output_ages.output_ages_address == input_idle_times.idle_time_address)

        miner_vectors_limit = 2000

        non_miner_vectors_limit = 20000


        false_miners = miners_join.join(miners,  "output_ages_address", "left_anti").limit(non_miner_vectors_limit)
        true_miners = miners_join.join(miners, "output_ages_address", "leftsemi").limit(miner_vectors_limit)

        false_miners = miners_join.withColumn("is_miner", F.lit("False")).select("is_miner",
                                                                                 miners_join.output_ages_address.alias(
                                                                                     "address"),
                                                                                 from_unixtime(unix_timestamp((minig_pool_class_df_output_ages.output_month_min).cast(
                                                                                     "timestamp"), "yyyy-MM-dd HH:mm:ss")).cast("timestamp").alias("output_month_min"),
                                                                                 from_unixtime(unix_timestamp((minig_pool_class_df_output_ages.output_month_max).cast(
                                                                                     "timestamp"), "yyyy-MM-dd HH:mm:ss")).cast("timestamp").alias("output_month_max"),
                                                                                 from_unixtime(unix_timestamp((minig_pool_class_df_input_ages.input_month_min).cast(
                                                                                     "timestamp"), "yyyy-MM-dd HH:mm:ss")).cast("timestamp").alias("input_month_min"),
                                                                                 from_unixtime(unix_timestamp((minig_pool_class_df_input_ages.input_month_max).cast(
                                                                                     "timestamp"), "yyyy-MM-dd HH:mm:ss")).cast("timestamp").alias("input_month_max"),
                                                                                 datediff(minig_pool_class_df_output_ages.output_month_max, minig_pool_class_df_output_ages.output_month_min).alias(
                                                                                     "output_active_time"),
                                                                                 datediff(minig_pool_class_df_input_ages.input_month_max,
                                                                                          minig_pool_class_df_input_ages.input_month_min).alias("input_active_time"),
                                                                                 datediff(minig_pool_class_df_output_ages.output_month_max,
                                                                                          minig_pool_class_df_input_ages.input_month_max).alias("io_max_lag"),
                                                                                 datediff(minig_pool_class_df_output_ages.output_month_min,
                                                                                          minig_pool_class_df_input_ages.input_month_min).alias("io_min_lag"),
                                                                                 minig_pool_class_df_output_monthly_stats.output_active_months,
                                                                                 minig_pool_class_df_output_monthly_stats.total_tx_output_count,
                                                                                 minig_pool_class_df_output_monthly_stats.total_tx_output_value,
                                                                                 minig_pool_class_df_output_monthly_stats.mean_tx_output_value,
                                                                                 minig_pool_class_df_output_monthly_stats.stddev_tx_output_value,
                                                                                 minig_pool_class_df_output_monthly_stats.total_output_tx,
                                                                                 minig_pool_class_df_output_monthly_stats.mean_monthly_output_value,
                                                                                 minig_pool_class_df_output_monthly_stats.mean_monthly_output_count,
                                                                                 minig_pool_class_df_input_monthly_stats.input_active_months,
                                                                                 minig_pool_class_df_input_monthly_stats.total_tx_input_count,
                                                                                 minig_pool_class_df_input_monthly_stats.total_tx_input_value,
                                                                                 minig_pool_class_df_input_monthly_stats.mean_tx_input_value,
                                                                                 minig_pool_class_df_input_monthly_stats.stddev_tx_input_value,
                                                                                 minig_pool_class_df_input_monthly_stats.total_input_tx,
                                                                                 minig_pool_class_df_input_monthly_stats.mean_monthly_input_value,
                                                                                 minig_pool_class_df_input_monthly_stats.mean_monthly_input_count,
                                                                                 output_idle_times.mean_output_idle_time,
                                                                                 output_idle_times.stddev_output_idle_time,
                                                                                 input_idle_times.mean_input_idle_time,
                                                                                 input_idle_times.stddev_input_idle_time)

        true_miners = miners_join.withColumn("is_miner", F.lit("True")).select("is_miner",
                                                                               miners_join.output_ages_address.alias(
                                                                                   "address"),
                                                                               from_unixtime(unix_timestamp((minig_pool_class_df_output_ages.output_month_min).cast(
                                                                                   "timestamp"), "yyyy-MM-dd HH:mm:ss")).cast("timestamp").alias("output_month_min"),
                                                                               from_unixtime(unix_timestamp((minig_pool_class_df_output_ages.output_month_max).cast(
                                                                                   "timestamp"), "yyyy-MM-dd HH:mm:ss")).cast("timestamp").alias("output_month_max"),
                                                                               from_unixtime(unix_timestamp((minig_pool_class_df_input_ages.input_month_min).cast(
                                                                                   "timestamp"), "yyyy-MM-dd HH:mm:ss")).cast("timestamp").alias("input_month_min"),
                                                                               from_unixtime(unix_timestamp((minig_pool_class_df_input_ages.input_month_max).cast(
                                                                                   "timestamp"), "yyyy-MM-dd HH:mm:ss")).cast("timestamp").alias("input_month_max"),
                                                                               datediff(minig_pool_class_df_output_ages.output_month_max, minig_pool_class_df_output_ages.output_month_min).alias(
                                                                                   "output_active_time"),
                                                                               datediff(minig_pool_class_df_input_ages.input_month_max,
                                                                                        minig_pool_class_df_input_ages.input_month_min).alias("input_active_time"),
                                                                               datediff(minig_pool_class_df_output_ages.output_month_max,
                                                                                        minig_pool_class_df_input_ages.input_month_max).alias("io_max_lag"),
                                                                               datediff(minig_pool_class_df_output_ages.output_month_min,
                                                                                        minig_pool_class_df_input_ages.input_month_min).alias("io_min_lag"),
                                                                               minig_pool_class_df_output_monthly_stats.output_active_months,
                                                                               minig_pool_class_df_output_monthly_stats.total_tx_output_count,
                                                                               minig_pool_class_df_output_monthly_stats.total_tx_output_value,
                                                                               minig_pool_class_df_output_monthly_stats.mean_tx_output_value,
                                                                               minig_pool_class_df_output_monthly_stats.stddev_tx_output_value,
                                                                               minig_pool_class_df_output_monthly_stats.total_output_tx,
                                                                               minig_pool_class_df_output_monthly_stats.mean_monthly_output_value,
                                                                               minig_pool_class_df_output_monthly_stats.mean_monthly_output_count,
                                                                               minig_pool_class_df_input_monthly_stats.input_active_months,
                                                                               minig_pool_class_df_input_monthly_stats.total_tx_input_count,
                                                                               minig_pool_class_df_input_monthly_stats.total_tx_input_value,
                                                                               minig_pool_class_df_input_monthly_stats.mean_tx_input_value,
                                                                               minig_pool_class_df_input_monthly_stats.stddev_tx_input_value,
                                                                               minig_pool_class_df_input_monthly_stats.total_input_tx,
                                                                               minig_pool_class_df_input_monthly_stats.mean_monthly_input_value,
                                                                               minig_pool_class_df_input_monthly_stats.mean_monthly_input_count,
                                                                               output_idle_times.mean_output_idle_time,
                                                                               output_idle_times.stddev_output_idle_time,
                                                                               input_idle_times.mean_input_idle_time,
                                                                               input_idle_times.stddev_input_idle_time)
        minig_pool_class_df = true_miners.unionAll(false_miners)


        logger.info('....Persist to BQ')  
        minig_pool_class_df.write.format('bigquery') \
        .mode("overwrite")\
            .option('table', minig_pool_class_table) \
        .save()

    except RuntimeError as coreError:
            logger.error(coreError)
    else:
        logger.info('Successfully completed preprocessing!')
# }} End fnMain()

def fnConfigureLogger():
# {{ Start 
    """
    Purpose:
        Configure a logger for the script
    Returns:
        Logger object
    """
    logFormatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("data_engineering")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logStreamHandler = logging.StreamHandler(sys.stdout)
    logStreamHandler.setFormatter(logFormatter)
    logger.addHandler(logStreamHandler)
    return logger
# }} End fnConfigureLogger()

if __name__ == "__main__":
    arguments = fnParseArguments()
    logger = fnConfigureLogger()
    fnMain(logger, arguments)