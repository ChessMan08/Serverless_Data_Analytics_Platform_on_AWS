import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Get job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_SOURCE', 'S3_DEST'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Create a DynamicFrame from the source S3 data
source_dynamic_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="csv",
    connection_options={"paths": [args['S3_SOURCE']], "recurse": True},
    format_options={"withHeader": True, "separator": ","},
    transformation_ctx="source_dynamic_frame"
)

# Write the data to the destination in Parquet format
glueContext.write_dynamic_frame.from_options(
    frame=source_dynamic_frame,
    connection_type="s3",
    connection_options={"path": args['S3_DEST']},
    format="parquet",
    transformation_ctx="write_dynamic_frame"
)

job.commit()
