# sqs-to-s3-micro2
## Function
Service that pulls messages from SQS queue and stores them in an S3 bucket as JSON files.

Add these GitHub repository secrets:
 - `AWS_ACCESS_KEY_ID`: Your AWS access key with permissions for:
   - SQS
   - S3
   - SSM Parameter Store
   - ECR
 - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
 - `AWS_REGION`: us-east-2 (or your preferred region)

For simplicity during testing, you might start with Admin access and then dial down permissions based on the resources defined in the Terraform files.

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
