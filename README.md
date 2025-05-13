# sqs-to-s3-micro2
## Function
Service that pulls messages from SQS queue and stores them in an S3 bucket as JSON files.

## Flow
1. Continuously checks the SQS queue for new messages
2. Retrieves queue URL from AWS Parameter Store
3. Checks if message is already processed (using S3 object existence)
4. Writes message content to S3 bucket as JSON files
5. Skips duplicate messages to prevent reprocessing


- Python (with boto3)
- AWS S3, SQS, SSM Parameter Store, ECR, ECS
- Docker container
- CI/CD via GitHub Actions workflow
