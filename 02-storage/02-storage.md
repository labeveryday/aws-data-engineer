# Storage

## 21-Intro Storage

## 22-Amazon S3

**Section Introduction:**
- Amazon S3 is one of the main building blocks of AWS
- It's advertised as **infinitely scaling** storage
- Many websites use Amazon S3 as a backbone
- Many AWS services use Amazon S3 as an integration as well

**Amazon S3 Use cases:**
- Backup and storage
- Disaster Recovery
- Archive
- Hybrid Cloud storage
- Application hosting
- Media hosting
- Data lakes & big data analytics
- Software delivery
- Static website

**Amazon S3 - Buckets**
- Amazon S3 allows people to store objects (files) in buckets (directories)
- Buckets must have a globally unique name (across all regions all accounts)
- Buckets are defined at the region level
- S3 looks like a global service but buckets are created in a region
- Naming convention
	- No uppercase, No underscore
	- 3-63 characters long
	- NOT an IP
	- Must start with lowercase letter or number
	- Must NOT start with the prefix `xn--`
	- Must NOT end with the suffix `-s3alias`

**Amazon S3 - Objects**
- Objects (files) have a Key
- The `key` is the FULL path:
	- *s3://my-bucket/==my_file.txt*
	- *s3://my-bucket/==my_folder/another_folder/my_file.txt*
- The key is composed of prefix + object name
	- *s3://my-bucket/my_folder/another_folder/my_file.txt*
- There's no concept of directories within buckets (although the UI will trick you to think otherwise)
- Just keys with very long names that contains slashes ("/")

- Object values are the content of the body:
	- Max. Object Size is 5TB (5000GB)
	- If uploading more than 5GB, must use multi-part upload
- Metadata (list of text key/value pairs - system or use metadata)
- Tags (Unicode key/value pair - up to 10) - useful for security /lifecycle
- Version ID (if versioning is enabled.)
## 23-Amazon S3 Hands On

- Create a S3 bucket (duan-demo-bucket-v1)
- from resources/code/s3 upload the coffee.jpeg file
- Open the object
- Create an images folder 
- upload the beach.jpeg file
- Delete the entire images folder

## 24-Amazon S3 Security - Bucket Policy

Amazon S3 - Security
- User-Based 
	- IAM Policies - which API calls should be allowed for a specific user from IAM
- Resource-Based
	- Bucket Policies - bucket wide rules from the S3 console - allows cross account
	- Object Access Control List (ACL) - finer grain (can be disabled)
	- Bucket Access Control List (ACL) - less common (can be disabled)

>NOTE: an IAM principal can access an S3 object if
> - The user IAM permissions ALLOW it OR the resource policy ALLOWS it 
> - AND there's no explicit DENY

- Encryption: encrypts objects in Amazon S3 using encryption keys

![](Screenshot%202024-05-21%20at%2011.42.25%20AM.png)
![](Screenshot%202024-05-21%20at%2011.43.03%20AM.png)

![](Screenshot%202024-05-21%20at%2011.43.36%20AM.png)

![](Screenshot%202024-05-21%20at%2011.44.14%20AM.png)
![](Screenshot%202024-05-21%20at%2011.44.29%20AM.png)

![](Screenshot%202024-05-21%20at%2011.45.38%20AM.png)

## 25-Amazon S3 Security - Bucket Policy - Hands On

- Open the S3 bucket (duan-demo-bucket-v1)
- All public access to the bucket
- Create a bucket policy to make the bucket policy using [aws policy generator](https://awspolicygen.s3.amazonaws.com/policygen.html) <-- This generates a policy

## 26-Amazon S3 Versioning

- You can version your files in Amazon S3
- It is enabled at the **bucket level**
- Same key overwrite will change the version: 1,2,3
- It is best practice to version your buckets
	- Protect against unintended deletes (ability to restore a version)
	- Easy roll back to previous version
- Notes:
	- Any file that is not versioned prior to enabling versioning will have version `null`
	- Suspending versioning does not delete the previous versions.

![](Screenshot%202024-05-21%20at%2011.54.57%20AM.png)
## 27-Amazon S3 Versioning Hands On

- Open the S3 bucket (duan-demo-bucket-v1)
- Click properties and enable versioning

![](Screenshot%202024-05-21%20at%2011.56.42%20AM.png)
## 28-Amazon S3 Replication

Amazon S3 - Replication (CRR & SRR)
- SetUp
	- Must enable Versioning in source and destination buckets
	- Cross-Region Replication (CRR)
		- Two different region
	- Same-Region Replication (SRR)
		- Same region
	- Buckets can be in different AWS accounts
	- Copying is asynchronous
	- Must give proper IAM permissions to S3
- Use cases:
	- CRR: - compliance, lower latency access, replication across accounts
	- SRR: - log aggregation, live replication between production and test accounts

## 29-Amazon S3 Replication - Notes

- After you enable Replication, only new objects are replicated
- Optionally, you can replicate existing objets using S3 Batch Replication
	- Replicates existing objects and objects that failed replication
- For DELETE operations
	- Can replicate delete markers from source to target (optional setting)
	- Deletions with a version ID are not replicated (to avoid malicious deletes)
- There is no **chaining** of replication
	- If bucket 1 has replication into bucket 2, which has replication into bucket 3
	- Then objects created in bucket 1 are not replicated into bucket 3

## 30-Amazon S3 Replication - Hands On

- Create a new bucket: `duan-demo-replica-bucket-v1` in a different region with versioning enabled.
- Enable versioning on duan-demo-bucket-v1
- Under management create a replication rule: `DemoReplicationRule`
	- Apply to all objects in the bucket
	- NOTE: Versioning needs to be enabled on both buckets

![](Screenshot%202024-05-21%20at%201.19.16%20PM.png)

## 31-Amazon S3 - Storage Classes

- Amazon S3 Standard - General Purpose
- Amazon S3 Standard-Infrequent Access (IA)
- Amazon S33 One Zone-Infrequent Access
- Amazon S3 Glacier Instant Retrieval
- Amazon S3 Glacier Flexible Retrieval
- Amazon S3 Glacier Deep Archive
- Amazon S3 Intelligent Tiering

You can move between classes manually or using S3 Lifecycle configurations.

S3 Durability and Availability
- Durability
	- High durability (99.999999999% 11 9's) of objects across multiple AZ
	- If you store 10,000,000 objects with Amazon S3, you can on average expect to incur a loss of a single object once every 10,000 years
	- Same for all storage classes.
- Availability:
	- Measures how readily available a service is
	- Varies depending on storage class
	- Example: S3 standard has 99.99% availability = not available 53 minutes a year. 

S3 Standard - General Purpose
- 99.99% Availability 
- Used for frequently accessed data
- Low latency and high throughput
- Sustain 2 concurrent facility failures

- Use Cases: Big Data analytics, mobile & gaming applications, content distribution... 

S3 Storage Classes - Infrequent Access
- For data that is less frequently accessed, but requires rapid access when needed
- Lower cost than S3 Standard
- Amazon S3 Standard-Infrequent Access (S3 Standard-IA)
	- 99% Availability 
	- Use cases: Disaster Recovery, backups
- Amazon S3 One Zone-Infrequent Access (S3 One Zone-IA)
	- High durability (99.999999999%) in a single AZ; data lost when AZ is destroyed

Amazon S3 Glacier Storage Classes
- Low-cost object storage meant for archiving / backup
- Pricing: price for storage + object retrieval cost
- Amazon S3 Glacier Instant Retrieval 
	- Millisecond retrieval, great for data accessed once a quarter
	- Minimum storage duration of 90 days
- Amazon S3 Glacier Flexible Retrieval (formerly Amazon S3 Glacier):
	- Expedited (1 to 5 minutes), Standard (3 to 5 hours)



## 32-Amazon S3 - Storage Classes - Hands On