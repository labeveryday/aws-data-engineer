# Lab 2.3: DynamoDB NoSQL Database Design

## Overview
This lab focuses on designing and implementing efficient NoSQL data models using Amazon DynamoDB. You will learn how to design tables with appropriate partition and sort keys, implement single-table design patterns, and optimize for common access patterns, which are essential skills for the AWS Certified Data Engineer exam.

**Learning Objectives:**
- Design DynamoDB tables with effective partition and sort keys
- Implement single-table design for multiple entity types
- Use secondary indexes for flexible query patterns
- Implement efficient data access patterns
- Optimize for performance and cost
- Understand DynamoDB capacity modes and scaling

**AWS Services Used:**
- Amazon DynamoDB
- AWS Lambda (optional for data loading)
- Amazon CloudWatch
- AWS Identity and Access Management (IAM)

**Estimated Time:** 2-3 hours

**Estimated Cost:** $1-5 (Most operations fall under Free Tier if available)

## Prerequisites
- AWS Account with appropriate permissions
- IAM permissions for DynamoDB
- Basic understanding of NoSQL concepts
- Familiarity with JSON data format

## Architecture Diagram
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │
│  DynamoDB   │────▶│  Global     │────▶│  DynamoDB   │
│  Table      │     │  Secondary  │     │  Streams    │
│             │     │  Index      │     │ (Optional)  │
│             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
       │                                       │
       │                                       │
       ▼                                       ▼
┌─────────────┐                         ┌─────────────┐
│             │                         │             │
│  Local      │                         │  Lambda     │
│  Secondary  │                         │  Function   │
│  Index      │                         │ (Optional)  │
│             │                         │             │
└─────────────┘                         └─────────────┘
```

## Implementation Steps

### Step 1: Plan Your Data Model and Access Patterns
1. For this lab, we'll create an e-commerce application with the following entities:
   - Customers
   - Products
   - Orders
   - Order Items

2. Define the key access patterns:
   - Get customer by ID
   - Get all orders for a customer
   - Get order details including items
   - Get all products in a category
   - Get product details by ID
   - Find orders by date range
   - Find top-selling products

3. Plan the single-table design:
   - Partition Key: A composite key with entity type and ID (e.g., "CUSTOMER#123")
   - Sort Key: Used for hierarchical relationships and filtering

### Step 2: Create the DynamoDB Table
1. Navigate to the Amazon DynamoDB console
2. Click "Create table"
3. Configure the table:
   - Table name: `EcommerceApp`
   - Partition key: `PK` (String)
   - Sort key: `SK` (String)
4. For capacity settings:
   - Choose "On-demand" for simplicity (or provisioned with auto-scaling for production)
5. Create the table and wait for it to become active

### Step 3: Create Secondary Indexes
1. After the table is created, go to the "Indexes" tab
2. Create a Global Secondary Index (GSI) for category-based queries:
   - Index name: `GSI1`
   - Partition key: `GSI1PK` (String)
   - Sort key: `GSI1SK` (String)
   - Projected attributes: All

3. Create another GSI for date-based queries:
   - Index name: `GSI2`
   - Partition key: `GSI2PK` (String)
   - Sort key: `GSI2SK` (String)
   - Projected attributes: All

### Step 4: Insert Customer Data
1. Go to the "Items" tab of your table
2. Click "Create item" and add the following JSON:

```json
{
  "PK": {"S": "CUSTOMER#1"},
  "SK": {"S": "METADATA"},
  "EntityType": {"S": "CUSTOMER"},
  "Name": {"S": "John Doe"},
  "Email": {"S": "john.doe@example.com"},
  "Address": {"S": "123 Main St, Seattle, WA 98101"},
  "Phone": {"S": "555-123-4567"},
  "RegistrationDate": {"S": "2023-01-15"},
  "GSI1PK": {"S": "CUSTOMER"},
  "GSI1SK": {"S": "John Doe"}
}
```

3. Add a few more customers:

```json
{
  "PK": {"S": "CUSTOMER#2"},
  "SK": {"S": "METADATA"},
  "EntityType": {"S": "CUSTOMER"},
  "Name": {"S": "Jane Smith"},
  "Email": {"S": "jane.smith@example.com"},
  "Address": {"S": "456 Oak Ave, Portland, OR 97205"},
  "Phone": {"S": "555-987-6543"},
  "RegistrationDate": {"S": "2023-02-20"},
  "GSI1PK": {"S": "CUSTOMER"},
  "GSI1SK": {"S": "Jane Smith"}
}
```

```json
{
  "PK": {"S": "CUSTOMER#3"},
  "SK": {"S": "METADATA"},
  "EntityType": {"S": "CUSTOMER"},
  "Name": {"S": "Robert Johnson"},
  "Email": {"S": "robert.j@example.com"},
  "Address": {"S": "789 Pine Rd, San Francisco, CA 94105"},
  "Phone": {"S": "555-456-7890"},
  "RegistrationDate": {"S": "2023-03-10"},
  "GSI1PK": {"S": "CUSTOMER"},
  "GSI1SK": {"S": "Robert Johnson"}
}
```

### Step 5: Insert Product Data
1. Add products with category information:

```json
{
  "PK": {"S": "PRODUCT#101"},
  "SK": {"S": "METADATA"},
  "EntityType": {"S": "PRODUCT"},
  "Name": {"S": "Laptop Pro"},
  "Category": {"S": "Electronics"},
  "Price": {"N": "1299.99"},
  "Description": {"S": "High-performance laptop with 16GB RAM"},
  "StockQuantity": {"N": "50"},
  "GSI1PK": {"S": "CATEGORY#Electronics"},
  "GSI1SK": {"S": "PRODUCT#Laptop Pro"}
}
```

```json
{
  "PK": {"S": "PRODUCT#102"},
  "SK": {"S": "METADATA"},
  "EntityType": {"S": "PRODUCT"},
  "Name": {"S": "Smartphone X"},
  "Category": {"S": "Electronics"},
  "Price": {"N": "899.99"},
  "Description": {"S": "Latest smartphone with advanced camera"},
  "StockQuantity": {"N": "100"},
  "GSI1PK": {"S": "CATEGORY#Electronics"},
  "GSI1SK": {"S": "PRODUCT#Smartphone X"}
}
```

```json
{
  "PK": {"S": "PRODUCT#103"},
  "SK": {"S": "METADATA"},
  "EntityType": {"S": "PRODUCT"},
  "Name": {"S": "Coffee Maker"},
  "Category": {"S": "Home Appliances"},
  "Price": {"N": "79.99"},
  "Description": {"S": "Programmable coffee maker with timer"},
  "StockQuantity": {"N": "30"},
  "GSI1PK": {"S": "CATEGORY#Home Appliances"},
  "GSI1SK": {"S": "PRODUCT#Coffee Maker"}
}
```

### Step 6: Insert Order Data with Hierarchical Relationships
1. Add an order with order items as separate records with the same partition key:

```json
{
  "PK": {"S": "ORDER#1001"},
  "SK": {"S": "METADATA"},
  "EntityType": {"S": "ORDER"},
  "CustomerID": {"S": "CUSTOMER#1"},
  "OrderDate": {"S": "2023-06-15"},
  "Status": {"S": "Delivered"},
  "TotalAmount": {"N": "1299.99"},
  "ShippingAddress": {"S": "123 Main St, Seattle, WA 98101"},
  "GSI1PK": {"S": "CUSTOMER#1"},
  "GSI1SK": {"S": "ORDER#2023-06-15"},
  "GSI2PK": {"S": "ORDER"},
  "GSI2SK": {"S": "2023-06-15"}
}
```

```json
{
  "PK": {"S": "ORDER#1001"},
  "SK": {"S": "ITEM#101"},
  "EntityType": {"S": "ORDER_ITEM"},
  "ProductID": {"S": "PRODUCT#101"},
  "ProductName": {"S": "Laptop Pro"},
  "Quantity": {"N": "1"},
  "Price": {"N": "1299.99"}
}
```

2. Add another order with multiple items:

```json
{
  "PK": {"S": "ORDER#1002"},
  "SK": {"S": "METADATA"},
  "EntityType": {"S": "ORDER"},
  "CustomerID": {"S": "CUSTOMER#2"},
  "OrderDate": {"S": "2023-06-20"},
  "Status": {"S": "Shipped"},
  "TotalAmount": {"N": "979.98"},
  "ShippingAddress": {"S": "456 Oak Ave, Portland, OR 97205"},
  "GSI1PK": {"S": "CUSTOMER#2"},
  "GSI1SK": {"S": "ORDER#2023-06-20"},
  "GSI2PK": {"S": "ORDER"},
  "GSI2SK": {"S": "2023-06-20"}
}
```

```json
{
  "PK": {"S": "ORDER#1002"},
  "SK": {"S": "ITEM#102"},
  "EntityType": {"S": "ORDER_ITEM"},
  "ProductID": {"S": "PRODUCT#102"},
  "ProductName": {"S": "Smartphone X"},
  "Quantity": {"N": "1"},
  "Price": {"N": "899.99"}
}
```

```json
{
  "PK": {"S": "ORDER#1002"},
  "SK": {"S": "ITEM#103"},
  "EntityType": {"S": "ORDER_ITEM"},
  "ProductID": {"S": "PRODUCT#103"},
  "ProductName": {"S": "Coffee Maker"},
  "Quantity": {"N": "1"},
  "Price": {"N": "79.99"}
}
```

### Step 7: Query the Data Using Different Access Patterns
1. Get a customer by ID:
   - Go to the "Items" tab
   - Click "Query"
   - Enter Partition key: `CUSTOMER#1`
   - Enter Sort key: `METADATA`

2. Get all orders for a customer (using GSI1):
   - Go to the "Indexes" tab
   - Select "GSI1"
   - Click "Query"
   - Enter Partition key: `CUSTOMER#1`
   - Enter Sort key begins with: `ORDER#`

3. Get order details including items:
   - Go to the "Items" tab
   - Click "Query"
   - Enter Partition key: `ORDER#1002`
   - Leave Sort key empty to get all items

4. Get all products in a category (using GSI1):
   - Go to the "Indexes" tab
   - Select "GSI1"
   - Click "Query"
   - Enter Partition key: `CATEGORY#Electronics`

5. Find orders by date range (using GSI2):
   - Go to the "Indexes" tab
   - Select "GSI2"
   - Click "Query"
   - Enter Partition key: `ORDER`
   - Enter Sort key between: `2023-06-01` and `2023-06-30`

### Step 8: Use PartiQL for SQL-like Queries
1. Go to the "PartiQL editor" tab
2. Run a query to find all customers:
   ```sql
   SELECT * FROM "EcommerceApp" WHERE "EntityType" = 'CUSTOMER'
   ```

3. Run a query to find a specific order:
   ```sql
   SELECT * FROM "EcommerceApp" WHERE "PK" = 'ORDER#1001'
   ```

4. Run a query to find products with price greater than 500:
   ```sql
   SELECT * FROM "EcommerceApp" WHERE "EntityType" = 'PRODUCT' AND "Price" > 500
   ```

### Step 9: Implement Conditional Updates
1. Go to the "Items" tab
2. Find the product with PK=`PRODUCT#101` and SK=`METADATA`
3. Click "Edit"
4. Change the StockQuantity to 45
5. Add a condition expression: `attribute_exists(PK) AND StockQuantity > :val`
6. Add expression attribute value: `:val` = `0` (Number)
7. Save the changes

### Step 10: Monitor DynamoDB Usage
1. Navigate to the CloudWatch console
2. Go to "Metrics" > "DynamoDB"
3. Check metrics for:
   - ConsumedReadCapacityUnits
   - ConsumedWriteCapacityUnits
   - SuccessfulRequestLatency

## Validation Steps
1. Verify that all data was inserted correctly
2. Confirm that queries using different access patterns return the expected results
3. Check that secondary indexes are working properly
4. Verify that conditional updates work as expected
5. Review CloudWatch metrics to understand resource usage

## Cleanup Instructions
1. Delete the DynamoDB table
   ```
   aws dynamodb delete-table --table-name EcommerceApp
   ```

## Challenge Extensions (Optional)
1. Implement DynamoDB Streams to capture table changes
2. Create a Lambda function to process stream events
3. Implement Time-To-Live (TTL) for temporary data
4. Set up DynamoDB Accelerator (DAX) for caching
5. Implement a more complex data model with additional entity types
6. Create a script to bulk load data from a CSV file

## Additional Resources
- [DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [Single-Table Design Pattern](https://aws.amazon.com/blogs/compute/creating-a-single-table-design-with-amazon-dynamodb/)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [Advanced DynamoDB Design Patterns](https://aws.amazon.com/blogs/database/amazon-dynamodb-advanced-design-patterns-for-microservices/)

## Notes and Tips
- Choose partition keys that distribute data evenly to avoid hot partitions
- Use sort keys to organize related items and enable efficient range queries
- Consider using composite sort keys (e.g., `ORDER#2023-06-15`) for flexible querying
- Keep item size small (ideally under 4KB) for better performance
- Use sparse indexes to reduce storage and write costs
- Remember that secondary indexes consume additional write capacity
- Use projection expressions to retrieve only the attributes you need
- Consider using DynamoDB Transactions for operations that require ACID compliance
