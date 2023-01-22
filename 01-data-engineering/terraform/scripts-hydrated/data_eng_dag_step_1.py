# ............................................................
# Preprocessing - Step 1
# ............................................................
# This script performs data preprocessing (step 1) from initial data in BigQuery
# and persists back to BigQuery
# ............................................................


import sys
import logging
import argparse
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
from pyspark.sql import functions as F
import pandas as pd
import numpy as np
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
    bqDatasetNm = f"{projectID}.crypto_bitcoin"
    appBaseName = "mining-pool-detector"
    appNameSuffix = "preprocessing"
    appName = f"{appBaseName}-{appNameSuffix}"
    scratchBucketUri = f"s8s-spark-bucket-{projectNbr}/{appBaseName}/pipelineId-{pipelineID}/{appNameSuffix}"
    sourceTableUriTransactions = '{}.crypto_bitcoin.transactions'.format(projectID)
    sourceTableUriBlocks = '{}.crypto_bitcoin.blocks'.format(projectID)
    miners_table = f"{bqDatasetNm}.miners"
    minig_pool_class_df_output_ages_table = f"{bqDatasetNm}.minig_pool_class_df_output_ages"
    minig_pool_class_df_input_ages_table = f"{bqDatasetNm}.minig_pool_class_df_input_ages"
    minig_pool_class_df_output_monthly_stats_table = f"{bqDatasetNm}.minig_pool_class_df_output_monthly_stats"
    minig_pool_class_df_input_monthly_stats_table = f"{bqDatasetNm}.minig_pool_class_df_input_monthly_stats"
    output_idle_times_table = f"{bqDatasetNm}.output_idle_times"
    input_idle_times_table = f"{bqDatasetNm}.input_idle_times"
    pipelineExecutionDt = datetime.now().strftime("%Y%m%d%H%M%S")

    # 1c. Display input and output
    if displayPrintStatements:
        logger.info("Starting STEP 1 data preprocessing for the *Mining Pool Classifier* pipeline")
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
        logger.info(f"....Source Data Transactions={sourceTableUriTransactions}")
        logger.info(f"....Source Data Blocks={sourceTableUriBlocks}")
        logger.info(f"....Scratch Bucket for BQ connector=gs://s8s-spark-bucket-{projectNbr}") 
        logger.info("OUTPUT-")
       

    try:
       
        logger.info('....Initializing spark & spark configs')
        spark = SparkSession.builder.appName(appName).getOrCreate()

        
        spark.conf.set("parentProject", projectID)
        spark.conf.set("temporaryGcsBucket", scratchBucketUri)

        
        logger.info('....Read source data')

        minig_pool_class_transactions_df = spark.read.format('bigquery').option('table', sourceTableUriTransactions).load()
        minig_pool_class_blocks_df = spark.read.format('bigquery').option('table', sourceTableUriBlocks).load()

        minig_pool_class_df_explode_outputs = minig_pool_class_transactions_df.withColumn("o", F.explode("outputs")).withColumn("o_address", F.explode("o.addresses"))
        minig_pool_class_df_explode_inputs = minig_pool_class_transactions_df.withColumn("i", F.explode("inputs")).withColumn("i_address", F.explode("i.addresses"))
        minig_pool_class_df_output_ages = minig_pool_class_df_explode_outputs.groupBy("o_address").agg(F.min("block_timestamp_month").alias("output_month_min"),  F.max("block_timestamp_month").alias("output_month_max")).select(minig_pool_class_df_explode_outputs.o_address.alias("output_ages_address"),"output_month_min","output_month_max")
        minig_pool_class_df_input_ages = minig_pool_class_df_explode_inputs.groupBy("i_address").agg(F.min("block_timestamp_month").alias("input_month_min"),  F.max("block_timestamp_month").alias("input_month_max")).select(minig_pool_class_df_explode_inputs.i_address.alias("input_ages_address"),"input_month_min","input_month_max")
        minig_pool_class_df_output_monthly_stats = minig_pool_class_df_explode_outputs.groupBy("o_address").agg( F.countDistinct("block_timestamp_month").alias("output_active_months"),F.count("outputs").alias("total_tx_output_count"), F.sum("output_value").alias("total_tx_output_value"), F.avg("output_value").alias("mean_tx_output_value"), F.stddev("output_value").alias("stddev_tx_output_value"), F.countDistinct("hash").alias("total_output_tx") , (F.sum("output_value")/F.count("block_timestamp_month")).alias("mean_monthly_output_value") , ( F.count("o.addresses") / F.count("block_timestamp_month")  ).alias("mean_monthly_output_count")   ).select(  minig_pool_class_df_explode_outputs.o_address.alias("output_monthly_stats_address"),"output_active_months","total_tx_output_count","total_tx_output_value","mean_tx_output_value","stddev_tx_output_value","total_output_tx","mean_monthly_output_value","mean_monthly_output_count")
        minig_pool_class_df_input_monthly_stats = minig_pool_class_df_explode_inputs.groupBy("i_address").agg( F.countDistinct("block_timestamp_month").alias("input_active_months"),F.count("inputs").alias("total_tx_input_count"), F.sum("input_value").alias("total_tx_input_value"), F.avg("input_value").alias("mean_tx_input_value"), F.stddev("input_value").alias("stddev_tx_input_value"), F.countDistinct("hash").alias("total_input_tx") , (F.sum("input_value")/F.count("block_timestamp_month")).alias("mean_monthly_input_value") , ( F.count("i.addresses") / F.count("block_timestamp_month")  ).alias("mean_monthly_input_count")   ).select(minig_pool_class_df_explode_inputs.i_address.alias("input_monthly_stats_address"),"input_active_months","total_tx_input_count","total_tx_input_value","mean_tx_input_value","stddev_tx_input_value","total_input_tx","mean_monthly_input_value","mean_monthly_input_count")


        output_window_spec = Window.partitionBy("o_address").orderBy("block_timestamp")
        output_event = minig_pool_class_df_explode_outputs.withColumn(
            "prev_block_time", lag("block_timestamp").over(output_window_spec))
        output_event = output_event.where(
            output_event.prev_block_time != output_event.block_timestamp)
        output_event = output_event.select("o_address", when(output_event.prev_block_time.isNull(), None).otherwise(
            unix_timestamp("block_timestamp") - unix_timestamp("prev_block_time")).alias("idle_time"))
        output_idle_times = output_event.groupBy("o_address").agg(F.avg("idle_time").alias("mean_output_idle_time"), F.stddev("idle_time").alias(
            "stddev_output_idle_time")).select(output_event.o_address.alias("idle_time_address"), "mean_output_idle_time", "stddev_output_idle_time")
        input_window_spec = Window.partitionBy("i_address").orderBy("block_timestamp")
        input_event = minig_pool_class_df_explode_inputs.withColumn(
            "prev_block_time", lag("block_timestamp").over(input_window_spec))
        input_event = input_event.where(
            input_event.prev_block_time != input_event.block_timestamp)
        input_event = input_event.select("i_address", when(input_event.prev_block_time.isNull(), None).otherwise(
            unix_timestamp("block_timestamp") - unix_timestamp("prev_block_time")).alias("idle_time"))
        input_idle_times = input_event.groupBy("i_address").agg(F.avg("idle_time").alias("mean_input_idle_time"), F.stddev("idle_time").alias(
            "stddev_input_idle_time")).select(input_event.i_address.alias("idle_time_address"), "mean_input_idle_time", "stddev_input_idle_time")
       
        miners = minig_pool_class_df_explode_outputs.join(
            minig_pool_class_blocks_df, minig_pool_class_df_explode_outputs.block_hash == minig_pool_class_blocks_df.hash)

        miners = miners.where(((miners.is_coinbase == True) & ((miners.coinbase_param.like('%4d696e656420627920416e74506f6f6c%')) |
                                                               (miners.coinbase_param.like('%2f42434d6f6e737465722f%')) |
                                                               (miners.coinbase_param.like('%4269744d696e746572%')) |
                                                               (miners.coinbase_param.like('%2f7374726174756d2f%')) |
                                                               (miners.coinbase_param.like('%456c6967697573%')) |
                                                               (miners.coinbase_param.like('%2f627261766f2d6d696e696e672f%')) |
                                                               (miners.coinbase_param.like('%4b616e6f%')) |
                                                               (miners.coinbase_param.like('%2f6d6d706f6f6c%')) |
                                                               (miners.coinbase_param.like('%2f736c7573682f%')))))

        miners = miners.groupBy("o_address").agg(
            F.count("o_address").alias("count_miners"))


        miners = miners.where(miners.count_miners > 20).select(
            miners.o_address.alias("output_ages_address"))


        miners.write.format('bigquery') \
        .mode("overwrite")\
            .option('table', miners_table) \
        .save()

        minig_pool_class_df_output_ages.write.format('bigquery') \
            .mode("overwrite")\
            .option('table', minig_pool_class_df_output_ages_table) \
            .save()

        minig_pool_class_df_input_ages.write.format('bigquery') \
            .mode("overwrite")\
            .option('table', minig_pool_class_df_input_ages_table) \
            .save()
        minig_pool_class_df_output_monthly_stats.write.format('bigquery') \
            .mode("overwrite")\
            .option('table', minig_pool_class_df_output_monthly_stats_table) \
            .save()

        minig_pool_class_df_input_monthly_stats.write.format('bigquery') \
            .mode("overwrite")\
            .option('table', minig_pool_class_df_input_monthly_stats_table) \
            .save()
        output_idle_times.write.format('bigquery') \
            .mode("overwrite")\
            .option('table', output_idle_times_table) \
            .save()

        input_idle_times.write.format('bigquery') \
            .mode("overwrite")\
            .option('table', input_idle_times_table) \
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