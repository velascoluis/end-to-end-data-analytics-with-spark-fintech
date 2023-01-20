from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, TimestampType
from pyspark.sql.functions import col, from_json, window
from pyspark.sql.functions import *
from pyspark.sql.types import *
import sys

# Arguments
kafkaTopicNm = sys.argv[1]
projectID = sys.argv[2]
bqScratchBucket = sys.argv[3]
checkpointGCSUri = sys.argv[4]
bqTable = sys.argv[5]
printArguments = sys.argv[6]

if printArguments:
    # {{
    print("Arguments:")
    print(f"kafkaTopicNm={kafkaTopicNm}")
    print(f"projectID={projectID}")
    print(f"bqScratchBucket={bqScratchBucket}")
    print(f"checkpointGCSUri={checkpointGCSUri}")
    print(f"bqTable={bqTable}")


# }}

# Spark session
spark = SparkSession \
    .builder \
    .appName("bitcoin-transactions") \
    .config("spark.streaming.stopGracefullyOnShutdown", "true") \
    .config("spark.sql.streaming.schemaInference", "true") \
    .getOrCreate()

# Config for use by Spark BQ connector
spark.conf.set("parentProject", projectID)
spark.conf.set("temporaryGcsBucket", bqScratchBucket)

# Create DataFrame from kafka
rawStreamingDF = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-cluster-w-0:9092") \
    .option("subscribe", kafkaTopicNm).option("failOnDataLoss", "false") \
    .load()


CastedStreamingDF = rawStreamingDF.selectExpr(
    "CAST(value AS STRING) as json_payload")


schema = StructType([
    StructField("timestamp", StringType()),
    StructField("name", StringType()),
    StructField("is_coinbase", StringType()),
    StructField("tx_value", StringType())

])


ParsedStreamingDF = CastedStreamingDF.withColumn(
    "jsonData", from_json(col("json_payload"), schema)).select("jsonData.*")

entriesStreamingDF = ParsedStreamingDF.toDF(
    "timestamp", "name", "is_coinbase", "tx_value")
entriesStreamingDF = entriesStreamingDF.withColumn(
    "tx_value", entriesStreamingDF.tx_value.cast('int'))
entriesStreamingDF = entriesStreamingDF.withColumn(
    "timestamp", entriesStreamingDF.tx_value.cast('timestamp'))
entriesStreamingAggDF = entriesStreamingDF.withWatermark("timestamp", "1 minutes").groupBy(
    entriesStreamingDF.is_coinbase, window(entriesStreamingDF.timestamp, "1 minutes")).count()
queryDF = entriesStreamingAggDF.writeStream.format("bigquery").outputMode(
    "complete").option("table", bqTable).option("checkpointLocation", checkpointGCSUri).start()
queryDF.awaitTermination()
