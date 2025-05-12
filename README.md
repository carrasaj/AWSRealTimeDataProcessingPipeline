# AWS Real-Time Data Processing Pipeline

## Overview
This project demonstrates a real-time and batch data processing pipeline built entirely on AWS. I utilize sample data, generated from a python script for this project. The pipeline processes real-time IoT-like streaming data, enriches it with metadata from batch data, and provides insights via Amazon QuickSight dashboards. I built this as my second AWS project to gain hands on experience with real time data streams using Kinesis and to learn QuickSight and Athena.

### Key AWS Services Used
- **Amazon Kinesis**: Captures real-time streaming data from simulated IoT devices.
- **AWS Lambda**: Processes and writes streaming data to S3 in NDJSON format.
- **Amazon S3**: Serves as a data lake to store raw and processed data.
- **AWS Glue**: Performs data transformation and schema discovery.
- **Amazon Athena**: Queries the processed data using SQL.
- **Amazon QuickSight**: Visualizes data insights for stakeholders.

---

## Architecture
The project implements the following architecture:

![Architecture Diagram](architecture/architecture_diagram.png)

### Architecture Description
1. **Real-Time Data Ingestion**:
   - Streaming data (e.g., IoT logs) is ingested into **Amazon Kinesis**.
   - **AWS Lambda** processes this data and stores it in S3 as NDJSON files.

2. **Batch Data Ingestion**:
   - Periodic CSV metadata files (e.g., device locations and types) are uploaded to S3.

3. **Data Transformation**:
   - **AWS Glue** joins streaming data with batch data, transforming it into a queryable format (Parquet).

4. **Data Querying**:
   - **Amazon Athena** queries enriched data stored in S3 for ad-hoc analysis.

5. **Data Visualization**:
   - **Amazon QuickSight** provides interactive dashboards to visualize temperature, humidity, and device statistics.

---

## Use Cases
This pipeline can be applied to a variety of real-world scenarios:
1. **IoT Monitoring**: Monitor sensor data in real time and correlate it with metadata for actionable insights.
2. **Application Logging**: Aggregate application logs to monitor performance and detect anomalies.
3. **Retail Analytics**: Combine real-time sales transactions with batch inventory updates to track trends and optimize stock levels.

---

## Key Features
- **Real-Time and Batch Integration**: Combines high-velocity streaming data with static metadata for enriched insights.
- **Scalable and Cost-Efficient**: Uses serverless AWS components that scale automatically with workload.
- **Actionable Visualizations**: Empowers stakeholders with interactive dashboards in QuickSight.

---

## Setup Instructions

### Prerequisites
- AWS Account
- AWS CLI Installed and Configured

### Steps to Replicate
1. **Set Up Kinesis Data Stream**:
   - Create a Kinesis stream named `my-streaming-logs`.

2. **Deploy AWS Lambda Function**:
   - Upload and configure the `producer.py` script to simulate streaming data.
   - Deploy the `lambda_function.py` to process and write data to S3.

3. **Create S3 Buckets**:
   - Create an S3 bucket for raw data (`raw/`) and processed data (`processed/`).

4. **Run Glue Crawlers**:
   - Configure Glue crawlers to discover schemas for streaming and batch data.

5. **Run Glue ETL Job**:
   - Deploy the `glue_etl_script.py` to transform and enrich data.

6. **Set Up QuickSight Dashboard**:
   - Import Athena datasets into QuickSight and create a dashboard.

---

## Files in This Repository
- `scripts/producer.py`: Simulates real-time streaming data.
- `scripts/lambda_function.py`: Processes streaming data and writes to S3.
- `scripts/glue_etl_script.py`: Enriches data and writes to S3 in Parquet format.
- `docs/use_cases.md`: Real-world use cases for this pipeline.
- `config/Athena_query_examples.sql`: Example SQL queries for Athena.

---

## Future Improvements
- Add support for real-time alerts using Amazon SNS.
- Implement automated batch metadata updates.
- Extend the pipeline to include machine learning predictions.

