# AWS Deployment Guide

This guide walks you through deploying Rowell Infra frontend and backend to AWS using GitHub Actions.

## Prerequisites

1. **AWS Account** with credits
2. **AWS CLI** installed and configured
3. **GitHub Repository** (public)

## Step 1: Setup AWS Resources

### Frontend Deployment (S3 + CloudFront)

```bash
# Create S3 bucket for frontend
aws s3 mb s3://rowell-infra-frontend --region us-east-1

# Enable static website hosting
aws s3 website s3://rowell-infra-frontend \
  --index-document index.html \
  --error-document index.html

# Create CloudFront distribution (optional but recommended)
# Use AWS Console or CLI to create distribution pointing to S3 bucket
```

### Backend Deployment (ECS or Elastic Beanstalk)

#### Option A: Elastic Container Service (ECS)

```bash
# Create ECR repository
aws ecr create-repository --repository-name rowell-infra-api --region us-east-1

# Create ECS cluster
aws ecs create-cluster --cluster-name rowell-infra-cluster

# Create task definition (use AWS Console or see docker-compose.yml)
# Create ECS service pointing to your cluster
```

#### Option B: Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize EB
cd api
eb init -p docker rowell-infra-api --region us-east-1

# Create environment
eb create rowell-infra-prod

# Get environment name for GitHub secrets
eb status
```

## Step 2: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:

```
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=rowell-infra-frontend
CLOUDFRONT_DISTRIBUTION_ID=E1234567890 (optional)
ECR_REPOSITORY_NAME=rowell-infra-api
ECS_CLUSTER_NAME=rowell-infra-cluster
ECS_SERVICE_NAME=rowell-infra-service
VITE_API_URL=https://api.your-domain.com
```

## Step 3: Create IAM User for GitHub Actions

```bash
# Create IAM user
aws iam create-user --user-name github-actions-rowell-infra

# Attach policies (minimal permissions needed)
aws iam attach-user-policy \
  --user-name github-actions-rowell-infra \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

aws iam attach-user-policy \
  --user-name github-actions-rowell-infra \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess

aws iam attach-user-policy \
  --user-name github-actions-rowell-infra \
  --policy-arn arn:aws:iam::aws:policy/AmazonECS_FullAccess

# Create access keys
aws iam create-access-key --user-name github-actions-rowell-infra
```

**Copy the Access Key ID and Secret Access Key** → Add to GitHub Secrets

## Step 4: Environment Variables for Backend

Configure environment variables in your deployment platform:

### For ECS Task Definition:
```json
{
  "environment": [
    {"name": "DATABASE_URL", "value": "postgresql+asyncpg://..."},
    {"name": "HEDERA_TESTNET_OPERATOR_ID", "value": "0.0.xxxxxxx"},
    {"name": "HEDERA_TESTNET_OPERATOR_KEY", "value": "302e..."},
    {"name": "SECRET_KEY", "value": "your-secret-key"},
    {"name": "BACKEND_CORS_ORIGINS", "value": "[\"https://your-frontend-domain.com\"]"}
  ]
}
```

### For Elastic Beanstalk:
```bash
eb setenv DATABASE_URL="postgresql+asyncpg://..."
eb setenv HEDERA_TESTNET_OPERATOR_ID="0.0.xxxxxxx"
eb setenv SECRET_KEY="your-secret-key"
```

## Step 5: Database Setup

### Option A: AWS RDS PostgreSQL

```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier rowell-infra-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username rowell \
  --master-user-password YourPassword123! \
  --allocated-storage 20
```

### Option B: External Database

Use your existing PostgreSQL database or managed service (like Supabase, Railway, etc.)

## Step 6: Test Deployment

1. **Push to main branch** to trigger workflows
2. **Monitor GitHub Actions** tab for deployment progress
3. **Verify Frontend**: Visit your S3 bucket URL or CloudFront distribution
4. **Verify Backend**: Check health endpoint `https://api.your-domain.com/health`

## Troubleshooting

### Frontend deployment fails
- Check S3 bucket permissions
- Verify CloudFront distribution exists (if using)
- Check build logs in GitHub Actions

### Backend deployment fails
- Verify ECR repository exists
- Check ECS service/EB environment is configured
- Review backend logs in CloudWatch

### Environment variables not loading
- Verify secrets are set in GitHub
- Check environment variables in ECS task definition or EB configuration

## Estimated Costs

- **S3 Storage**: ~$0.023/GB/month (frontend is ~5MB = ~$0.0001/month)
- **CloudFront**: ~$0.085/GB transfer (first 10TB free)
- **ECS/EB**: ~$15-30/month for t3.small instance
- **RDS**: ~$15/month for db.t3.micro
- **Total**: ~$30-45/month for full deployment

With AWS credits, this should be well within budget!

