# Serverless Data Analytics Platform on AWS

This repository contains the complete source code and infrastructure definition for a scalable, end-to-end serverless data analytics platform on AWS. The platform ingests, processes, and analyzes both real-time clickstream data and batch advertising data, making it available for querying through standard SQL.

---

## Architecture

The platform follows an event-driven architecture, leveraging a suite of managed AWS services to provide a cost-effective and highly scalable solution.



**Data Flow:**

1.  **Ingestion**: A Python producer script simulates real-time clickstream data and sends it to **Amazon Kinesis**. Batch advertising data is uploaded directly to an **S3** bucket.
2.  **Real-Time Processing**: The Kinesis stream triggers an **AWS Lambda** function, which performs initial data cleaning and transformation, saving the results to an S3 data lake in JSON format.
3.  **Batch Processing**: **AWS Glue** runs an ETL job to process the raw advertising data from S3, converting it into the optimized Apache Parquet format.
4.  **Analytics**: An **AWS Glue Crawler** scans the processed data in S3 and populates the AWS Glue Data Catalog. **Amazon Athena** is then used to run standard SQL queries on this data.

---

## Key Features

* **Dual Data Pipelines**: Handles both high-throughput real-time streaming data and large-volume batch data.
* **Fully Serverless**: No servers to manage, providing automatic scaling and a pay-per-use cost model.
* **Infrastructure as Code (IaC)**: The entire infrastructure is defined and deployed using **AWS CloudFormation**, enabling consistency and repeatability.
* **Data Lake on S3**: Uses Amazon S3 as a central, durable, and cost-effective data lake for raw and processed data.
* **Optimized for Analytics**: Converts raw data into formats like Apache Parquet to significantly speed up query performance and reduce costs.

---

## Technology Stack

* **Data Ingestion**: Amazon Kinesis, Python (Boto3)
* **Data Processing**: AWS Lambda, AWS Glue
* **Storage**: Amazon S3
* **Analytics**: Amazon Athena, AWS Glue Data Catalog
* **Deployment**: AWS CloudFormation, AWS CLI

---

## Deployment

### Prerequisites

1.  An active **AWS Account**.
2.  **AWS CLI** installed and configured.
3.  **Python 3** and `boto3` installed locally.

### Instructions

The entire infrastructure is deployed using the provided CloudFormation template.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ChessMan08/Serverless_Data_Analytics_Platform_on_AWS.git
    cd serverless-analytics-platform
    ```

2.  **Deploy the CloudFormation stack:**
    Choose a unique name for your data lake S3 bucket and run the following command.

    ```bash
    aws cloudformation deploy \
    --template-file cloudformation/template.yaml \
    --stack-name serverless-analytics-platform \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides DataLakeBucketName=<your-unique-bucket-name>
    ```
    This command will create all the necessary AWS resources automatically.

---

## Usage

### 1. Process Batch Data

* **Upload the sample data:** Manually upload the `data/ad_impressions.csv` file to the `raw-data` folder in the S3 bucket created by CloudFormation.
* **Run the Glue Job:** Navigate to the AWS Glue console, find the `Batch-Ad-Data-Processor` job, and run it. This job is defined in `scripts/etl/csv_to_parquet_converter.py`.

### 2. Process Real-Time Data

* **Install producer dependencies:**

    ```bash
    pip install -r scripts/producer/requirements.txt
    ```
* **Run the producer script:** This script will send simulated clickstream data to your Kinesis stream. Remember to set the correct AWS region inside the script if it's different from `us-east-1`.

    ```bash
    python scripts/producer/clickstream_producer.py
    ```

### 3. Query Your Data

* **Run the Glue Crawler:** In the AWS Glue console, run the `analytics-crawler` to catalog both the batch and real-time processed data.
* **Analyze with Athena:** Navigate to the Amazon Athena console. You should see the `analytics_db` database with two tables: `batch` and `realtime`. You can now run standard SQL queries on them.

    ```sql
    -- Query batch advertising data
    SELECT * FROM "analytics_db"."batch" LIMIT 10;

    -- Query real-time clickstream data
    SELECT * FROM "analytics_db"."realtime" LIMIT 10;
    ```

---

## Cleanup

To avoid ongoing charges, you can destroy all the created resources by deleting the CloudFormation stack.

```bash
aws cloudformation delete-stack --stack-name serverless-analytics-platform
```

## LICENSE

This project is licensed under the MIT License. You are free to use, modify, and distribute this software under the terms of the `MIT License`.
