# Step-by-Step AWS Backend Deployment Guide

This guide walks you through deploying the Rowell Infra backend API to AWS using ECS (Elastic Container Service) or Elastic Beanstalk.

## Prerequisites

- AWS Account with credits
- AWS CLI installed and configured (`aws configure`)
- Docker installed locally (for testing)
- GitHub repository (for CI/CD)

---

## Option 1: Deploy to AWS ECS (Recommended)

### Step 1: Create ECR Repository

```bash
# Set your AWS region
export AWS_REGION=us-east-1

# Create ECR repository
aws ecr create-repository \
  --repository-name rowell-infra-api \
  --region $AWS_REGION \
  --image-scanning-configuration scanOnPush=true

# Get repository URI (save this!)
aws ecr describe-repositories \
  --repository-names rowell-infra-api \
  --region $AWS_REGION \
  --query 'repositories[0].repositoryUri' \
  --output text
```

**Output will look like**: `123456789012.dkr.ecr.us-east-1.amazonaws.com/rowell-infra-api`

### Step 2: Build and Push Docker Image Locally (Test)

```bash
cd api

# Authenticate Docker to ECR
aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Build the image
docker build -t rowell-infra-api .

# Tag for ECR
docker tag rowell-infra-api:latest \
  123456789012.dkr.ecr.us-east-1.amazonaws.com/rowell-infra-api:latest

# Push to ECR
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/rowell-infra-api:latest
```

### Step 3: Create ECS Cluster

```bash
# Create cluster
aws ecs create-cluster \
  --cluster-name rowell-infra-cluster \
  --region $AWS_REGION
```

### Step 4: Create VPC and Networking (if needed)

```bash
# Create VPC (or use default)
aws ec2 create-vpc \
  --cidr-block 10.0.0.0/16 \
  --region $AWS_REGION

# Note the VPC ID from output

# Create Internet Gateway
aws ec2 create-internet-gateway --region $AWS_REGION

# Create Public Subnets (for Fargate)
aws ec2 create-subnet \
  --vpc-id vpc-xxxxx \
  --cidr-block 10.0.1.0/24 \
  --availability-zone ${AWS_REGION}a \
  --region $AWS_REGION

aws ec2 create-subnet \
  --vpc-id vpc-xxxxx \
  --cidr-block 10.0.2.0/24 \
  --availability-zone ${AWS_REGION}b \
  --region $AWS_REGION

# Create Security Group
aws ec2 create-security-group \
  --group-name rowell-infra-sg \
  --description "Security group for Rowell Infra API" \
  --vpc-id vpc-xxxxx \
  --region $AWS_REGION

# Allow HTTP and HTTPS traffic
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0 \
  --region $AWS_REGION

aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0 \
  --region $AWS_REGION
```

### Step 5: Create Task Definition

Create file `task-definition.json`:

```json
{
  "family": "rowell-infra-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::YOUR_ACCOUNT_ID:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::YOUR_ACCOUNT_ID:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "rowell-infra-api",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/rowell-infra-api:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql+asyncpg://user:pass@host:5432/dbname"
        },
        {
          "name": "REDIS_URL",
          "value": "redis://your-redis-host:6379/0"
        },
        {
          "name": "HEDERA_TESTNET_OPERATOR_ID",
          "value": "0.0.xxxxxxx"
        },
        {
          "name": "SECRET_KEY",
          "value": "your-secret-key-here"
        },
        {
          "name": "BACKEND_CORS_ORIGINS",
          "value": "[\"https://your-frontend-domain.com\"]"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/rowell-infra-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**Register the task definition:**

```bash
aws ecs register-task-definition \
  --cli-input-json file://task-definition.json \
  --region $AWS_REGION
```

### Step 6: Create ECS Service

```bash
aws ecs create-service \
  --cluster rowell-infra-cluster \
  --service-name rowell-infra-service \
  --task-definition rowell-infra-api \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx,subnet-yyyyy],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}" \
  --region $AWS_REGION
```

### Step 7: Create Application Load Balancer (Optional but Recommended)

```bash
# Create load balancer
aws elbv2 create-load-balancer \
  --name rowell-infra-alb \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-groups sg-xxxxx \
  --region $AWS_REGION

# Get load balancer ARN from output

# Create target group
aws elbv2 create-target-group \
  --name rowell-infra-targets \
  --protocol HTTP \
  --port 8000 \
  --vpc-id vpc-xxxxx \
  --target-type ip \
  --health-check-path /health \
  --region $AWS_REGION

# Create listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:... \
  --region $AWS_REGION

# Update ECS service to use load balancer
aws ecs update-service \
  --cluster rowell-infra-cluster \
  --service rowell-infra-service \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=rowell-infra-api,containerPort=8000" \
  --region $AWS_REGION
```

### Step 8: Get Your API URL

```bash
# Get load balancer DNS name
aws elbv2 describe-load-balancers \
  --names rowell-infra-alb \
  --query 'LoadBalancers[0].DNSName' \
  --output text \
  --region $AWS_REGION
```

Your API will be available at: `http://rowell-infra-alb-xxxxx.us-east-1.elb.amazonaws.com`

---

## Option 2: Deploy to Elastic Beanstalk (Easier)

### Step 1: Install EB CLI

```bash
pip install awsebcli
```

### Step 2: Initialize EB in Your Project

```bash
cd api
eb init -p docker -r us-east-1 rowell-infra-api
```

This will:
- Ask for AWS credentials (or use existing)
- Create application name: `rowell-infra-api`
- Select region: `us-east-1`
- Create `.elasticbeanstalk/` directory

### Step 3: Create EB Environment

```bash
# Create environment with Docker platform
eb create rowell-infra-prod \
  --platform docker \
  --instance-type t3.small \
  --envvars DATABASE_URL="postgresql+asyncpg://...",SECRET_KEY="...",HEDERA_TESTNET_OPERATOR_ID="0.0.xxxxxxx"
```

### Step 4: Deploy

```bash
# Build and deploy
eb deploy

# Or deploy specific version
eb deploy rowell-infra-prod
```

### Step 5: Get Your API URL

```bash
eb status
```

Look for `CNAME` in output: `rowell-infra-prod.us-east-1.elasticbeanstalk.com`

### Step 6: Set Environment Variables

```bash
# Set all environment variables
eb setenv \
  DATABASE_URL="postgresql+asyncpg://user:pass@host:5432/db" \
  REDIS_URL="redis://host:6379/0" \
  HEDERA_TESTNET_OPERATOR_ID="0.0.xxxxxxx" \
  HEDERA_TESTNET_OPERATOR_KEY="302e..." \
  SECRET_KEY="your-secret-key" \
  JWT_SECRET_KEY="your-jwt-secret" \
  BACKEND_CORS_ORIGINS='["https://your-frontend.com"]'
```

---

## Step-by-Step: Setup Database (RDS PostgreSQL)

### Step 1: Create RDS Database

```bash
# Create DB subnet group (use existing VPC)
aws rds create-db-subnet-group \
  --db-subnet-group-name rowell-infra-db-subnet \
  --db-subnet-group-description "Subnet group for Rowell Infra DB" \
  --subnet-ids subnet-xxxxx subnet-yyyyy \
  --region $AWS_REGION

# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier rowell-infra-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15.4 \
  --master-username rowell \
  --master-user-password YourSecurePassword123! \
  --allocated-storage 20 \
  --storage-type gp2 \
  --vpc-security-group-ids sg-xxxxx \
  --db-subnet-group-name rowell-infra-db-subnet \
  --backup-retention-period 7 \
  --region $AWS_REGION
```

**Wait for database to be available** (5-10 minutes):

```bash
aws rds describe-db-instances \
  --db-instance-identifier rowell-infra-db \
  --query 'DBInstances[0].DBInstanceStatus' \
  --region $AWS_REGION
```

### Step 2: Get Database Endpoint

```bash
aws rds describe-db-instances \
  --db-instance-identifier rowell-infra-db \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text \
  --region $AWS_REGION
```

**Output**: `rowell-infra-db.xxxxx.us-east-1.rds.amazonaws.com`

### Step 3: Update Environment Variables

Update your ECS task definition or EB environment with:

```bash
DATABASE_URL=postgresql+asyncpg://rowell:YourSecurePassword123!@rowell-infra-db.xxxxx.us-east-1.rds.amazonaws.com:5432/rowell_infra
```

### Step 4: Initialize Database Schema

```bash
# SSH into ECS task or EB instance
# Then run:
python manage_db.py init
```

Or use EB:

```bash
eb ssh
cd /var/app/current
python manage_db.py init
```

---

## Step-by-Step: Setup Redis (ElastiCache)

### Step 1: Create ElastiCache Subnet Group

```bash
aws elasticache create-cache-subnet-group \
  --cache-subnet-group-name rowell-infra-redis-subnet \
  --cache-subnet-group-description "Subnet group for Rowell Infra Redis" \
  --subnet-ids subnet-xxxxx subnet-yyyyy \
  --region $AWS_REGION
```

### Step 2: Create ElastiCache Cluster

```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id rowell-infra-redis \
  --engine redis \
  --cache-node-type cache.t3.micro \
  --num-cache-nodes 1 \
  --cache-subnet-group-name rowell-infra-redis-subnet \
  --security-group-ids sg-xxxxx \
  --region $AWS_REGION
```

### Step 3: Get Redis Endpoint

```bash
aws elasticache describe-cache-clusters \
  --cache-cluster-id rowell-infra-redis \
  --show-cache-node-info \
  --query 'CacheClusters[0].CacheNodes[0].Endpoint.Address' \
  --output text \
  --region $AWS_REGION
```

### Step 4: Update Environment Variables

```bash
REDIS_URL=redis://rowell-infra-redis.xxxxx.cache.amazonaws.com:6379/0
```

---

## Configure GitHub Actions Secrets

Go to GitHub → Your Repository → Settings → Secrets and variables → Actions

Add these secrets:

```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
ECR_REPOSITORY_NAME=rowell-infra-api
ECR_REGISTRY=123456789012.dkr.ecr.us-east-1.amazonaws.com
ECS_CLUSTER_NAME=rowell-infra-cluster
ECS_SERVICE_NAME=rowell-infra-service
EB_ENVIRONMENT_NAME=rowell-infra-prod (if using EB)
```

---

## Verify Deployment

### Step 1: Test Health Endpoint

```bash
# For ECS with ALB
curl http://your-alb-dns-name/health

# For Elastic Beanstalk
curl http://rowell-infra-prod.us-east-1.elasticbeanstalk.com/health
```

### Step 2: Check Logs

**ECS:**
```bash
aws logs tail /ecs/rowell-infra-api --follow --region $AWS_REGION
```

**EB:**
```bash
eb logs
```

### Step 3: Test API Endpoint

```bash
curl -X GET "http://your-api-url/docs"
```

Should show Swagger UI.

---

## Troubleshooting

### Issue: Container fails to start
- Check CloudWatch logs
- Verify environment variables are set correctly
- Ensure database connection string is correct

### Issue: Can't connect to database
- Check security group allows traffic from ECS/EB to RDS
- Verify database endpoint is correct
- Check database password

### Issue: Deployment timeout
- Increase timeout in task definition
- Check if image builds successfully locally first

### Issue: Out of memory
- Increase memory in task definition (512MB → 1024MB)

---

## Cost Estimate

- **ECS Fargate**: ~$15/month (256 CPU, 512MB RAM, 1 task)
- **RDS db.t3.micro**: ~$15/month
- **ElastiCache cache.t3.micro**: ~$15/month
- **Application Load Balancer**: ~$20/month
- **Data Transfer**: ~$5/month (first 1GB free)

**Total**: ~$70/month (or use AWS credits!)

---

## Quick Reference Commands

```bash
# Check ECS service status
aws ecs describe-services \
  --cluster rowell-infra-cluster \
  --services rowell-infra-service \
  --region us-east-1

# Update service (force new deployment)
aws ecs update-service \
  --cluster rowell-infra-cluster \
  --service rowell-infra-service \
  --force-new-deployment \
  --region us-east-1

# View EB environment info
eb status
eb health

# Deploy new version (EB)
eb deploy

# View logs (EB)
eb logs
```

---

**Next Steps**: After backend is deployed, update frontend `VITE_API_URL` to point to your backend URL!

