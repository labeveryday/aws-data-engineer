# Lab 1.2: Streaming Data with Amazon Kinesis

## Overview
This lab focuses on building a real-time data streaming pipeline using Amazon Kinesis. You will learn how to ingest, process, and analyze streaming data in near real-time, which is a critical skill for the AWS Certified Data Engineer exam.

**Learning Objectives:**
- Set up Amazon Kinesis Data Streams for data ingestion
- Configure Kinesis Data Firehose for delivery to S3
- Process streaming data with Kinesis Data Analytics
- Implement basic stream processing with SQL
- Monitor streaming data pipelines

**AWS Services Used:**
- Amazon Kinesis Data Streams
- Amazon Kinesis Data Firehose
- Amazon Kinesis Data Analytics
- Amazon S3
- AWS Lambda (optional)
- Amazon CloudWatch

**Estimated Time:** 2-3 hours

**Estimated Cost:** $5-10 (Kinesis services have hourly charges)

## Prerequisites
- AWS Account with appropriate permissions
- IAM permissions for Kinesis, S3, and CloudWatch
- Basic understanding of streaming concepts
- Basic SQL knowledge for Kinesis Analytics

## Architecture Diagram
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │     │             │
│  Data       │────▶│  Kinesis    │────▶│  Kinesis    │────▶│  S3 Bucket  │
│  Producer   │     │  Streams    │     │  Firehose   │     │             │
│             │     │             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │
                          │
                          ▼
                    ┌─────────────┐     ┌─────────────┐
                    │             │     │             │
                    │  Kinesis    │────▶│  CloudWatch │
                    │  Analytics  │     │  Dashboard  │
                    │             │     │             │
                    └─────────────┘     └─────────────┘
```

## Implementation Steps

### Step 1: Create an S3 Bucket for Stream Data
1. Sign in to the AWS Management Console and navigate to the S3 service
2. Create a new S3 bucket with a unique name (e.g., `your-name-stream-data-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-stream-data-YYYYMMDD
   ```
3. Create the following folder structure:
   ```
   aws s3api put-object --bucket your-name-stream-data-YYYYMMDD --key raw-stream/
   aws s3api put-object --bucket your-name-stream-data-YYYYMMDD --key processed-stream/
   ```

### Step 2: Create a Kinesis Data Stream
1. Navigate to the Amazon Kinesis console
2. Select "Data Streams" and click "Create data stream"
3. Name the stream `sensor-data-stream`
4. Set the capacity mode to "On-demand"
5. Click "Create data stream" and wait for it to become active

### Step 3: Create a Kinesis Data Firehose Delivery Stream
1. In the Kinesis console, select "Delivery streams" and click "Create delivery stream"
2. Name the delivery stream `sensor-data-delivery`
3. For source, select "Amazon Kinesis Data Streams" and choose the `sensor-data-stream` you created
4. For destination, select "Amazon S3"
5. Choose the S3 bucket you created and set the prefix: `raw-stream/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/`
6. Set the buffer interval to 60 seconds and buffer size to 1 MB for this lab
7. Create or select an IAM role with appropriate permissions
8. Review and create the delivery stream

### Step 4: Create a Data Producer
1. For this lab, we'll use a simple Python script to generate simulated IoT sensor data
2. Create a file named `sensor_data_producer.py` with the following content:

```python
import json
import random
import time
import boto3
from datetime import datetime

# Initialize Kinesis client
kinesis_client = boto3.client('kinesis', region_name='us-east-1')  # Change to your region

# Sensor IDs
sensor_ids = ['sensor-' + str(i).zfill(3) for i in range(1, 11)]

# Function to generate random sensor data
def generate_sensor_data():
    sensor_id = random.choice(sensor_ids)
    timestamp = datetime.utcnow().isoformat()
    temperature = round(random.uniform(10.0, 40.0), 2)
    humidity = round(random.uniform(30.0, 90.0), 2)
    pressure = round(random.uniform(980.0, 1030.0), 2)
    
    return {
        'sensor_id': sensor_id,
        'timestamp': timestamp,
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure
    }

# Main loop to send data to Kinesis
def send_data_to_kinesis(stream_name, duration_seconds=300, delay=0.5):
    end_time = time.time() + duration_seconds
    records_sent = 0
    
    print(f"Sending data to Kinesis stream '{stream_name}' for {duration_seconds} seconds...")
    
    while time.time() < end_time:
        data = generate_sensor_data()
        partition_key = data['sensor_id']
        
        response = kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),
            PartitionKey=partition_key
        )
        
        records_sent += 1
        if records_sent % 20 == 0:
            print(f"Sent {records_sent} records to Kinesis")
        
        time.sleep(delay)
    
    print(f"Data generation complete. Sent {records_sent} records to Kinesis.")

if __name__ == "__main__":
    # Replace with your stream name
    stream_name = 'sensor-data-stream'
    
    # Send data for 5 minutes (300 seconds) with 0.5 second delay between records
    send_data_to_kinesis(stream_name, duration_seconds=300, delay=0.5)
```

3. Install the required AWS SDK:
   ```
   pip install boto3
   ```

4. Run the script to start sending data to your Kinesis stream:
   ```
   python sensor_data_producer.py
   ```

### Step 5: Create a Kinesis Data Analytics Application
1. Navigate to the Kinesis console and select "Analytics applications"
2. Click "Create analytics application"
3. Name the application `sensor-data-analytics`
4. Choose "SQL" for the runtime
5. Create or select an IAM role with appropriate permissions
6. For source, select the Kinesis data stream you created
7. After the application is created, go to "Real-time analytics" and click "Configure"
8. The console will automatically detect the schema from your stream data
9. In the SQL editor, enter the following query to calculate average temperature by sensor over a 1-minute window:

```sql
CREATE OR REPLACE STREAM "DESTINATION_SQL_STREAM" (
    sensor_id VARCHAR(20),
    avg_temperature DOUBLE,
    min_temperature DOUBLE,
    max_temperature DOUBLE,
    avg_humidity DOUBLE,
    window_start_time VARCHAR(50),
    window_end_time VARCHAR(50)
);

CREATE OR REPLACE PUMP "STREAM_PUMP" AS 
INSERT INTO "DESTINATION_SQL_STREAM"
SELECT STREAM
    sensor_id,
    AVG(temperature) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    AVG(humidity) AS avg_humidity,
    SUBSTRING(ROWTIME TO SECOND) AS window_start_time,
    SUBSTRING(ROWTIME + INTERVAL '1' MINUTE TO SECOND) AS window_end_time
FROM "SOURCE_SQL_STREAM_001"
GROUP BY 
    sensor_id,
    FLOOR(ROWTIME TO MINUTE);
```

10. Save and run the SQL query

### Step 6: Create a Second Firehose Delivery Stream for Processed Data
1. Create another Kinesis Firehose delivery stream named `processed-sensor-data`
2. For source, select "Kinesis Data Analytics" and choose your analytics application
3. For destination, select "Amazon S3"
4. Choose the S3 bucket you created and set the prefix: `processed-stream/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/`
5. Configure the buffer settings and IAM role as before
6. Review and create the delivery stream

### Step 7: Monitor Your Streaming Pipeline
1. Navigate to the CloudWatch console
2. Create a dashboard named `Streaming-Pipeline-Dashboard`
3. Add widgets to monitor:
   - Kinesis Data Stream metrics (PutRecord.Success, GetRecords.Success)
   - Kinesis Firehose delivery metrics (DeliveryToS3.Success)
   - Kinesis Analytics application metrics (success, failure)
4. Save the dashboard

### Step 8: Verify Data Flow
1. After running the data producer for a few minutes, check your S3 bucket
2. You should see data appearing in both the raw-stream and processed-stream folders
3. Download and examine a few files to verify the data format and content

## Validation Steps
1. Verify that records are being sent to the Kinesis data stream (check CloudWatch metrics)
2. Confirm that Firehose is delivering raw data to the S3 bucket
3. Check that the Kinesis Analytics application is processing data correctly
4. Verify that processed data is being delivered to the processed-stream folder in S3
5. Examine the CloudWatch dashboard to ensure all components are functioning

## Cleanup Instructions
1. Stop the Kinesis Analytics application
   ```
   aws kinesisanalytics stop-application --application-name sensor-data-analytics --force
   ```

2. Delete the Kinesis Analytics application
   ```
   aws kinesisanalytics delete-application --application-name sensor-data-analytics --force
   ```

3. Delete the Firehose delivery streams
   ```
   aws firehose delete-delivery-stream --delivery-stream-name sensor-data-delivery
   aws firehose delete-delivery-stream --delivery-stream-name processed-sensor-data
   ```

4. Delete the Kinesis data stream
   ```
   aws kinesis delete-stream --stream-name sensor-data-stream
   ```

5. Delete the S3 bucket and its contents
   ```
   aws s3 rb s3://your-name-stream-data-YYYYMMDD --force
   ```

6. Delete the CloudWatch dashboard
   ```
   aws cloudwatch delete-dashboards --dashboard-names Streaming-Pipeline-Dashboard
   ```

## Challenge Extensions (Optional)
1. Modify the data producer to simulate anomalies and create alerts using CloudWatch Alarms
2. Add a Lambda function to process records from the Kinesis stream in real-time
3. Implement error handling and dead-letter queues for failed records
4. Create a real-time visualization of the streaming data using Amazon QuickSight
5. Implement a consumer application using the Kinesis Client Library (KCL)

## Additional Resources
- [Amazon Kinesis Developer Guide](https://docs.aws.amazon.com/streams/latest/dev/introduction.html)
- [Kinesis Data Analytics SQL Reference](https://docs.aws.amazon.com/kinesisanalytics/latest/dev/analytics-sql-reference.html)
- [Real-time Streaming ETL with Kinesis](https://aws.amazon.com/blogs/big-data/create-real-time-streaming-etl-pipelines-with-amazon-kinesis-data-analytics-for-sql/)
- [Best Practices for Kinesis Data Streams](https://docs.aws.amazon.com/streams/latest/dev/kinesis-producer-adv-best-practices.html)

## Notes and Tips
- Kinesis Data Streams has a default retention period of 24 hours (can be extended to 7 days)
- For production workloads, consider using enhanced fan-out consumers for higher throughput
- Monitor shard utilization to determine when to scale your Kinesis stream
- Kinesis Analytics SQL has specific timestamp handling - review the documentation for details
- Remember to clean up resources after completing the lab to avoid ongoing charges
