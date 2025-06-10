# Lab 3.2: Stream Processing with Kinesis Analytics

## Overview
This lab focuses on real-time stream processing using Amazon Kinesis Data Analytics. You will learn how to analyze streaming data in real-time using SQL and implement windowed aggregations, which are essential skills for the AWS Certified Data Engineer exam.

**Learning Objectives:**
- Set up Kinesis Data Streams for data ingestion
- Configure Kinesis Data Analytics applications using SQL
- Implement real-time analytics on streaming data
- Create windowed aggregations and time-based analysis
- Process and transform streaming data
- Output processed results to destinations
- Monitor streaming analytics applications

**AWS Services Used:**
- Amazon Kinesis Data Streams
- Amazon Kinesis Data Analytics
- Amazon Kinesis Data Firehose
- Amazon S3
- AWS Lambda (optional)
- Amazon CloudWatch

**Estimated Time:** 2-3 hours

**Estimated Cost:** $5-10 (Kinesis services have hourly charges)

## Prerequisites
- AWS Account with appropriate permissions
- IAM permissions for Kinesis services, S3, and CloudWatch
- Basic understanding of SQL
- Familiarity with streaming concepts
- Basic Python knowledge for data generation

## Architecture Diagram
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │     │             │
│  Data       │────▶│  Kinesis    │────▶│  Kinesis    │────▶│  Kinesis    │
│  Generator  │     │  Data       │     │  Data       │     │  Data       │
│  (Python)   │     │  Streams    │     │  Analytics  │     │  Firehose   │
│             │     │             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                              │                    │
                                              │                    │
                                              ▼                    ▼
                                        ┌─────────────┐     ┌─────────────┐
                                        │             │     │             │
                                        │  CloudWatch │     │  S3 Bucket  │
                                        │  Dashboard  │     │             │
                                        │             │     │             │
                                        └─────────────┘     └─────────────┘
```

## Implementation Steps

### Step 1: Create S3 Bucket for Output Data
1. Sign in to the AWS Management Console and navigate to the S3 service
2. Create a new S3 bucket with a unique name (e.g., `your-name-stream-analytics-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-stream-analytics-YYYYMMDD
   ```
3. Create the following folder structure:
   ```
   aws s3api put-object --bucket your-name-stream-analytics-YYYYMMDD --key raw-data/
   aws s3api put-object --bucket your-name-stream-analytics-YYYYMMDD --key processed-data/
   ```

### Step 2: Create an IAM Role for Kinesis Services
1. Navigate to the IAM console
2. Create a new role with the following permissions:
   - AmazonKinesisFullAccess
   - AmazonKinesisAnalyticsFullAccess
   - AmazonKinesisFirehoseFullAccess
   - AmazonS3FullAccess (in production, use more restrictive policies)
   - CloudWatchFullAccess
3. Name the role `KinesisAnalyticsLabRole`

### Step 3: Create a Kinesis Data Stream
1. Navigate to the Amazon Kinesis console
2. Select "Data Streams" and click "Create data stream"
3. Name the stream `iot-sensor-stream`
4. Set the capacity mode to "On-demand"
5. Click "Create data stream" and wait for it to become active

### Step 4: Create a Kinesis Data Firehose Delivery Stream
1. In the Kinesis console, select "Delivery streams" and click "Create delivery stream"
2. Name the delivery stream `processed-sensor-data`
3. For source, select "Amazon Kinesis Data Streams" and choose the `iot-sensor-stream` you created
4. For destination, select "Amazon S3"
5. Choose the S3 bucket you created and set the prefix: `processed-data/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/`
6. Set the buffer interval to 60 seconds and buffer size to 1 MB for this lab
7. Create or select the IAM role you created earlier
8. Review and create the delivery stream

### Step 5: Create a Python Script to Generate Streaming Data
1. Create a file named `sensor_data_generator.py` with the following content:

```python
import json
import random
import time
import boto3
from datetime import datetime

# Initialize Kinesis client
kinesis_client = boto3.client('kinesis', region_name='us-east-1')  # Change to your region

# Sensor IDs and types
sensor_ids = [f'sensor-{i:03d}' for i in range(1, 21)]
sensor_types = ['temperature', 'humidity', 'pressure', 'motion', 'light']
locations = ['building-A', 'building-B', 'building-C']
floors = ['floor-1', 'floor-2', 'floor-3']
rooms = ['room-101', 'room-102', 'room-103', 'room-201', 'room-202', 'room-203']

# Function to generate random sensor data
def generate_sensor_data():
    sensor_id = random.choice(sensor_ids)
    sensor_type = random.choice(sensor_types)
    location = random.choice(locations)
    floor = random.choice(floors)
    room = random.choice(rooms)
    timestamp = datetime.utcnow().isoformat()
    
    # Generate reading based on sensor type
    if sensor_type == 'temperature':
        reading = round(random.uniform(15.0, 35.0), 2)  # Celsius
        status = 'alert' if reading > 30.0 else 'normal'
    elif sensor_type == 'humidity':
        reading = round(random.uniform(30.0, 90.0), 2)  # Percentage
        status = 'alert' if reading > 80.0 else 'normal'
    elif sensor_type == 'pressure':
        reading = round(random.uniform(980.0, 1030.0), 2)  # hPa
        status = 'alert' if reading < 990.0 or reading > 1020.0 else 'normal'
    elif sensor_type == 'motion':
        reading = random.choice([0, 1])  # 0=no motion, 1=motion detected
        status = 'alert' if reading == 1 else 'normal'
    else:  # light
        reading = round(random.uniform(0.0, 1000.0), 2)  # Lux
        status = 'alert' if reading < 100.0 else 'normal'
    
    return {
        'sensor_id': sensor_id,
        'sensor_type': sensor_type,
        'location': location,
        'floor': floor,
        'room': room,
        'timestamp': timestamp,
        'reading': reading,
        'status': status
    }

# Main loop to send data to Kinesis
def send_data_to_kinesis(stream_name, duration_seconds=300, delay=0.2):
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
        if records_sent % 50 == 0:
            print(f"Sent {records_sent} records to Kinesis")
        
        time.sleep(delay)
    
    print(f"Data generation complete. Sent {records_sent} records to Kinesis.")

if __name__ == "__main__":
    # Replace with your stream name
    stream_name = 'iot-sensor-stream'
    
    # Send data for 5 minutes (300 seconds) with 0.2 second delay between records
    send_data_to_kinesis(stream_name, duration_seconds=300, delay=0.2)
```

2. Install the required AWS SDK:
   ```
   pip install boto3
   ```

3. Run the script to start sending data to your Kinesis stream:
   ```
   python sensor_data_generator.py
   ```

### Step 6: Create a Kinesis Data Analytics Application
1. Navigate to the Kinesis console and select "Analytics applications"
2. Click "Create application"
3. Choose "SQL" for the application type
4. Name the application `iot-sensor-analytics`
5. Create or select the IAM role you created earlier
6. Click "Create application"

### Step 7: Configure the Analytics Application
1. After the application is created, click "Configure"
2. For source, select the Kinesis data stream you created (`iot-sensor-stream`)
3. Click "Discover schema" to automatically detect the schema from your stream data
4. After the schema is discovered, click "Save and continue"
5. In the "Real-time analytics" tab, click "Go to SQL editor"
6. Click "Yes, start application" to start the application

### Step 8: Create SQL Queries for Real-time Analytics
1. In the SQL editor, replace the default code with the following SQL queries:

```sql
-- Create destination streams for processed data
CREATE OR REPLACE STREAM "DESTINATION_SQL_STREAM" (
    sensor_type VARCHAR(16),
    location VARCHAR(16),
    floor VARCHAR(16),
    avg_reading DOUBLE,
    min_reading DOUBLE,
    max_reading DOUBLE,
    alert_count INTEGER,
    total_count INTEGER,
    alert_percentage DOUBLE,
    window_start_time TIMESTAMP,
    window_end_time TIMESTAMP
);

-- Create a pump to insert into output stream
CREATE OR REPLACE PUMP "STREAM_PUMP" AS 
INSERT INTO "DESTINATION_SQL_STREAM"
-- Aggregate data over 1-minute tumbling windows
SELECT STREAM
    sensor_type,
    location,
    floor,
    AVG(reading) AS avg_reading,
    MIN(reading) AS min_reading,
    MAX(reading) AS max_reading,
    SUM(CASE WHEN status = 'alert' THEN 1 ELSE 0 END) AS alert_count,
    COUNT(*) AS total_count,
    (SUM(CASE WHEN status = 'alert' THEN 1 ELSE 0 END) * 100.0) / COUNT(*) AS alert_percentage,
    FLOOR(ROWTIME TO MINUTE) AS window_start_time,
    FLOOR(ROWTIME TO MINUTE) + INTERVAL '1' MINUTE AS window_end_time
FROM "SOURCE_SQL_STREAM_001"
-- Group by sensor type, location, and floor
GROUP BY 
    sensor_type,
    location,
    floor,
    FLOOR(ROWTIME TO MINUTE);

-- Create a separate stream for anomaly detection
CREATE OR REPLACE STREAM "ANOMALY_SQL_STREAM" (
    sensor_id VARCHAR(16),
    sensor_type VARCHAR(16),
    location VARCHAR(16),
    floor VARCHAR(16),
    room VARCHAR(16),
    reading DOUBLE,
    status VARCHAR(16),
    event_time TIMESTAMP
);

-- Create a pump for anomaly detection
CREATE OR REPLACE PUMP "ANOMALY_PUMP" AS 
INSERT INTO "ANOMALY_SQL_STREAM"
-- Detect anomalies based on specific thresholds
SELECT STREAM
    sensor_id,
    sensor_type,
    location,
    floor,
    room,
    reading,
    status,
    ROWTIME AS event_time
FROM "SOURCE_SQL_STREAM_001"
WHERE 
    (sensor_type = 'temperature' AND reading > 30.0) OR
    (sensor_type = 'humidity' AND reading > 80.0) OR
    (sensor_type = 'pressure' AND (reading < 990.0 OR reading > 1020.0)) OR
    (sensor_type = 'motion' AND reading = 1) OR
    (sensor_type = 'light' AND reading < 100.0);
```

2. Click "Save and run SQL" to execute the queries

### Step 9: Configure Output for the Analytics Application
1. Go back to the application details page
2. Click "Connect to a destination"
3. Select "Kinesis Data Firehose" as the destination
4. Choose the `processed-sensor-data` delivery stream you created earlier
5. For the in-application stream, select `DESTINATION_SQL_STREAM`
6. Click "Save and continue"

### Step 10: Create a CloudWatch Dashboard for Monitoring
1. Navigate to the CloudWatch console
2. Click "Dashboards" and then "Create dashboard"
3. Name the dashboard `IoT-Sensor-Analytics-Dashboard`
4. Add widgets to monitor:
   - Kinesis Data Stream metrics (IncomingRecords, GetRecords.Success)
   - Kinesis Data Analytics metrics (InputRecords, OutputRecords)
   - Kinesis Data Firehose metrics (DeliveryToS3.Success)
5. Create custom metrics for sensor readings by location and type

### Step 11: Analyze the Results
1. After running the data generator for a few minutes, check your S3 bucket
2. You should see processed data files in the `processed-data` folder
3. Download and examine a few files to verify the aggregated data
4. Check the CloudWatch dashboard to monitor the streaming pipeline

### Step 12: Extend the Analytics with Additional Queries (Optional)
1. Go back to the SQL editor in your Kinesis Analytics application
2. Add the following SQL query to perform more advanced analytics:

```sql
-- Create a stream for detecting trends
CREATE OR REPLACE STREAM "TREND_SQL_STREAM" (
    sensor_type VARCHAR(16),
    location VARCHAR(16),
    current_avg DOUBLE,
    previous_avg DOUBLE,
    change_percentage DOUBLE,
    trend VARCHAR(16),
    window_start_time TIMESTAMP,
    window_end_time TIMESTAMP
);

-- Create a pump for trend analysis
CREATE OR REPLACE PUMP "TREND_PUMP" AS 
INSERT INTO "TREND_SQL_STREAM"
-- Compare current window with previous window
SELECT STREAM
    curr.sensor_type,
    curr.location,
    curr.avg_reading AS current_avg,
    prev.avg_reading AS previous_avg,
    ((curr.avg_reading - prev.avg_reading) / prev.avg_reading) * 100.0 AS change_percentage,
    CASE 
        WHEN curr.avg_reading > prev.avg_reading * 1.05 THEN 'rising'
        WHEN curr.avg_reading < prev.avg_reading * 0.95 THEN 'falling'
        ELSE 'stable'
    END AS trend,
    curr.window_start_time,
    curr.window_end_time
FROM 
    -- Current window aggregation
    (SELECT 
        sensor_type,
        location,
        AVG(reading) AS avg_reading,
        FLOOR(ROWTIME TO MINUTE) AS window_start_time,
        FLOOR(ROWTIME TO MINUTE) + INTERVAL '1' MINUTE AS window_end_time
    FROM "SOURCE_SQL_STREAM_001"
    GROUP BY 
        sensor_type,
        location,
        FLOOR(ROWTIME TO MINUTE)
    ) AS curr
JOIN 
    -- Previous window aggregation
    (SELECT 
        sensor_type,
        location,
        AVG(reading) AS avg_reading,
        FLOOR(ROWTIME TO MINUTE) - INTERVAL '1' MINUTE AS window_start_time,
        FLOOR(ROWTIME TO MINUTE) AS window_end_time
    FROM "SOURCE_SQL_STREAM_001"
    GROUP BY 
        sensor_type,
        location,
        FLOOR(ROWTIME TO MINUTE) - INTERVAL '1' MINUTE
    ) AS prev
ON 
    curr.sensor_type = prev.sensor_type AND
    curr.location = prev.location AND
    curr.window_start_time = prev.window_end_time;
```

3. Click "Save and run SQL" to execute the updated queries

## Validation Steps
1. Verify that data is flowing through the entire pipeline
2. Confirm that the Kinesis Analytics application is processing data correctly
3. Check that aggregated data is being delivered to S3
4. Verify that the CloudWatch dashboard shows the expected metrics
5. Examine the processed data files to ensure they contain the aggregated results
6. Check that anomaly detection is working as expected

## Cleanup Instructions
1. Stop the Kinesis Analytics application
   ```
   aws kinesisanalytics stop-application --application-name iot-sensor-analytics --force
   ```
2. Delete the Kinesis Analytics application
   ```
   aws kinesisanalytics delete-application --application-name iot-sensor-analytics --force
   ```
3. Delete the Kinesis Firehose delivery stream
   ```
   aws firehose delete-delivery-stream --delivery-stream-name processed-sensor-data
   ```
4. Delete the Kinesis data stream
   ```
   aws kinesis delete-stream --stream-name iot-sensor-stream
   ```
5. Delete the S3 bucket and its contents
   ```
   aws s3 rb s3://your-name-stream-analytics-YYYYMMDD --force
   ```
6. Delete the CloudWatch dashboard
   ```
   aws cloudwatch delete-dashboards --dashboard-names IoT-Sensor-Analytics-Dashboard
   ```
7. Delete the IAM role
   ```
   aws iam delete-role --role-name KinesisAnalyticsLabRole
   ```

## Challenge Extensions (Optional)
1. Implement a Lambda function to process anomalies in real-time
2. Create alerts based on anomaly detection using SNS
3. Visualize the streaming data in real-time using Amazon QuickSight
4. Implement machine learning for anomaly detection using RANDOM_CUT_FOREST
5. Create a web dashboard to display real-time analytics
6. Implement a feedback loop where analytics results trigger actions in the source system

## Additional Resources
- [Kinesis Data Analytics Developer Guide](https://docs.aws.amazon.com/kinesisanalytics/latest/dev/what-is.html)
- [Kinesis Data Analytics SQL Reference](https://docs.aws.amazon.com/kinesisanalytics/latest/dev/analytics-sql-reference.html)
- [Real-time Anomaly Detection with Kinesis Analytics](https://aws.amazon.com/blogs/big-data/real-time-anomaly-detection-using-amazon-kinesis-analytics/)
- [Streaming ETL with Kinesis](https://aws.amazon.com/blogs/big-data/create-real-time-streaming-etl-pipelines-with-amazon-kinesis-data-analytics-for-sql/)

## Notes and Tips
- Kinesis Data Analytics SQL is based on SQL but has some unique features for stream processing
- Window functions are crucial for aggregating streaming data over time periods
- Use appropriate timestamp handling for time-based analytics
- Monitor memory usage in your Kinesis Analytics application
- Consider using reference data to enrich your streaming data
- For production workloads, implement proper error handling and dead-letter queues
- Use CloudWatch alarms to monitor for anomalies in your streaming pipeline
