# Command-Line Deployment Scripts

These scripts automate the deployment of Rowell Infra backend to AWS.

## Quick Start

```bash
# 1. Setup AWS resources (ECR, ECS, VPC, etc.)
./scripts/setup-aws-resources.sh

# 2. Deploy backend
./scripts/deploy-backend-aws.sh
```

## Prerequisites

1. **AWS CLI installed and configured**
   ```bash
   aws configure
   # Enter your AWS Access Key ID
   # Enter your AWS Secret Access Key
   # Enter default region (e.g., us-east-1)
   ```

2. **Docker installed** (for building images)

3. **Git** (for version tags)

## Scripts Overview

### `setup-aws-resources.sh`
Creates all necessary AWS infrastructure:
- ECR repository (Docker image storage)
- ECS cluster
- VPC and subnets (if needed)
- Security groups
- CloudWatch log groups

**Usage:**
```bash
./scripts/setup-aws-resources.sh
```

**Environment Variables:**
- `AWS_REGION` - AWS region (default: us-east-1)

### `deploy-backend-aws.sh`
Deploys the backend application to AWS:
- Builds Docker image
- Pushes to ECR
- Creates/updates ECS service or Elastic Beanstalk environment
- Configures environment variables

**Usage:**
```bash
./scripts/deploy-backend-aws.sh
```

**What it does:**
1. Checks prerequisites (AWS CLI, Docker, credentials)
2. Asks you to choose: ECS or Elastic Beanstalk
3. Builds and pushes Docker image
4. Creates/updates deployment
5. Shows you the API URL

**Interactive prompts:**
- Deployment method (ECS or EB)
- Database URL
- Redis URL
- Hedera credentials
- Secret keys
- CORS origins

## Example Deployment Flow

### Option 1: ECS Deployment (Recommended)

```bash
# Step 1: Setup infrastructure
./scripts/setup-aws-resources.sh

# Step 2: Deploy
./scripts/deploy-backend-aws.sh
# Choose option 1 (ECS)
# Enter your configuration when prompted
```

**Output:**
```
✓ Deployment successful!

Service Details:
  Cluster: rowell-infra-cluster
  Service: rowell-infra-api
  Public IP: 54.123.45.67
  API URL: http://54.123.45.67:8000
  Health Check: http://54.123.45.67:8000/health
  Docs: http://54.123.45.67:8000/docs
```

### Option 2: Elastic Beanstalk Deployment

```bash
# Step 1: Setup infrastructure (optional for EB)
./scripts/setup-aws-resources.sh

# Step 2: Deploy
./scripts/deploy-backend-aws.sh
# Choose option 2 (Elastic Beanstalk)
# Enter your configuration when prompted
```

**Output:**
```
✓ Deployment successful!

Service Details:
  Environment: rowell-infra-api
  URL: http://rowell-infra-api.us-east-1.elasticbeanstalk.com
  Health Check: http://rowell-infra-api.us-east-1.elasticbeanstalk.com/health
  Docs: http://rowell-infra-api.us-east-1.elasticbeanstalk.com/docs
```

## Configuration

### Environment Variables

You can set these before running scripts:

```bash
export AWS_REGION=us-east-1
export PROJECT_NAME=rowell-infra  # Optional, default is rowell-infra
```

### Required Information

Before deployment, have ready:

1. **Database URL**
   - Format: `postgresql+asyncpg://user:password@host:5432/dbname`
   - Or use AWS RDS (setup separately)

2. **Redis URL**
   - Format: `redis://host:6379/0`
   - Or use AWS ElastiCache (setup separately)

3. **Hedera Credentials**
   - Operator ID: `0.0.xxxxxxx` (from portal.hedera.com)
   - Operator Key: `302e...` (private key)

4. **Secret Keys**
   - Secret Key (for API encryption)
   - JWT Secret Key (for authentication)

5. **CORS Origins**
   - Your frontend URL(s), comma-separated
   - Example: `https://app.example.com,https://www.example.com`

## Updating Deployment

To update after code changes:

```bash
# Just run the deploy script again
./scripts/deploy-backend-aws.sh

# It will:
# - Build new Docker image
# - Push to ECR
# - Update ECS service (forces new deployment)
```

## Troubleshooting

### Issue: "AWS credentials not configured"
```bash
aws configure
# Enter your credentials
```

### Issue: "Docker build fails"
- Check Docker is running: `docker ps`
- Check you're in the `api/` directory context

### Issue: "ECR push fails"
- Verify ECR repository exists: `aws ecr describe-repositories`
- Check you're authenticated: `aws ecr get-login-password`

### Issue: "Service fails to start"
- Check CloudWatch logs: `aws logs tail /ecs/rowell-infra-api --follow`
- Verify environment variables are set correctly
- Check database connectivity

### Issue: "Can't access API"
- Check security group allows port 8000
- Verify public IP is assigned (for ECS Fargate)
- Check load balancer (if using ALB)

## Viewing Logs

### ECS Logs
```bash
aws logs tail /ecs/rowell-infra-api --follow --region us-east-1
```

### Elastic Beanstalk Logs
```bash
cd api
eb logs rowell-infra-api
```

## Manual Steps (Optional)

### Create RDS Database
```bash
aws rds create-db-instance \
  --db-instance-identifier rowell-infra-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username rowell \
  --master-user-password YourPassword123! \
  --allocated-storage 20 \
  --region us-east-1
```

### Create ElastiCache Redis
```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id rowell-infra-redis \
  --engine redis \
  --cache-node-type cache.t3.micro \
  --num-cache-nodes 1 \
  --region us-east-1
```

Then use the endpoints in your deployment configuration.

## Next Steps

After backend is deployed:

1. **Update frontend** with backend URL
2. **Set GitHub Actions secrets** for CI/CD
3. **Configure custom domain** (optional)
4. **Setup monitoring** (CloudWatch alarms)

## Cost Estimates

- **ECS Fargate**: ~$15/month (1 task, 256 CPU, 512MB RAM)
- **RDS db.t3.micro**: ~$15/month
- **ElastiCache cache.t3.micro**: ~$15/month
- **Total**: ~$45/month (or use AWS credits!)

---

**Need help?** Check `BACKEND_AWS_DEPLOYMENT.md` for detailed manual steps.

