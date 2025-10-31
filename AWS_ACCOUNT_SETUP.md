# AWS Account Setup Guide for Backend Deployment

This guide walks you through setting up an AWS account, configuring credentials, and preparing for backend deployment.

---

## Step 1: Create/Access AWS Account

### If you don't have an AWS account:

1. **Go to AWS Sign Up**
   - Visit: https://aws.amazon.com/free/
   - Click "Create a Free Account"
   
2. **Fill in your details**
   - Email address
   - Password
   - Account name (e.g., "Rowell Infra")
   
3. **Enter payment information**
   - Credit card required (won't be charged if you stay in free tier or use credits)
   - For hackathon credits: Enter your card, but costs should be covered by credits
   
4. **Verify your identity**
   - Phone verification required
   
5. **Select support plan**
   - Choose "Basic Plan" (free) for now
   
6. **Account created!**
   - You'll receive a confirmation email
   - Log in to AWS Console: https://console.aws.amazon.com

### If you already have an AWS account:

- Log in at: https://console.aws.amazon.com

---

## Step 2: Apply AWS Credits (If Available)

If you have AWS credits from the hackathon:

1. **Go to AWS Billing Console**
   - https://console.aws.amazon.com/billing/

2. **Apply credits**
   - Click "Credits" in left menu
   - Click "Redeem Credit Code"
   - Enter your credit code
   - Credits will be applied to your account

3. **Set up billing alerts** (Important!)
   - Go to "Billing Preferences"
   - Enable "Receive Billing Alerts"
   - Go to CloudWatch → Billing Alarms
   - Create alarm if spending exceeds your credit amount

---

## Step 3: Choose AWS Region

For this deployment, we'll use **US East (N. Virginia) - us-east-1** (cheapest, best availability).

1. **Check region**
   - Look at top-right corner of AWS Console
   - Ensure it's set to "US East (N. Virginia)"
   - Or choose a region closer to your users

**Common regions:**
- `us-east-1` - US East (N. Virginia) - **Recommended (cheapest)**
- `us-west-2` - US West (Oregon)
- `eu-west-1` - Europe (Ireland)
- `ap-southeast-1` - Asia Pacific (Singapore)

---

## Step 4: Install AWS CLI

The AWS CLI allows you to deploy from command line.

### On Linux:

```bash
# Install AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify installation
aws --version
```

### On macOS:

```bash
# Using Homebrew
brew install awscli

# Or download installer
# https://awscli.amazonaws.com/AWSCLIV2.pkg

# Verify installation
aws --version
```

### On Windows:

1. Download installer: https://awscli.amazonaws.com/AWSCLIV2.msi
2. Run installer
3. Open Command Prompt
4. Verify: `aws --version`

---

## Step 5: Create IAM User for Deployment

**Important**: Never use your root AWS account credentials for deployment. Create an IAM user instead.

### Option A: Using AWS Console (Recommended for Beginners)

1. **Go to IAM Console**
   - https://console.aws.amazon.com/iam/
   - Or search "IAM" in AWS Console search bar

2. **Create IAM User**
   - Click "Users" in left menu
   - Click "Create user"
   - User name: `rowell-infra-deployment`
   - Check "Provide user access to the AWS Management Console" (optional)
   - Click "Next"

3. **Set Permissions**
   - Select "Attach policies directly"
   - Search and select these policies:
     - `AmazonEC2ContainerRegistryFullAccess` (for ECR)
     - `AmazonECS_FullAccess` (for ECS)
     - `AmazonElasticBeanstalkFullAccess` (if using EB)
     - `AmazonRDSFullAccess` (for database)
     - `AmazonElastiCacheFullAccess` (for Redis)
     - `CloudWatchLogsFullAccess` (for logging)
     - `IAMFullAccess` (for creating roles - use cautiously)
   
   **Or use a more restrictive custom policy** (see Step 6)
   
   - Click "Next"
   - Review and click "Create user"

4. **Create Access Keys**
   - Click on the user you just created
   - Go to "Security credentials" tab
   - Scroll to "Access keys"
   - Click "Create access key"
   - Choose "Command Line Interface (CLI)"
   - Check the confirmation box
   - Click "Next"
   - **Important**: Click "Download .csv file" or copy:
     - **Access Key ID**: `AKIA...`
     - **Secret Access Key**: `xxxx...` (save this now - you can't see it again!)
   - Click "Done"

### Option B: Using AWS CLI (Advanced)

```bash
# Create IAM user
aws iam create-user --user-name rowell-infra-deployment

# Attach policies
aws iam attach-user-policy \
  --user-name rowell-infra-deployment \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess

aws iam attach-user-policy \
  --user-name rowell-infra-deployment \
  --policy-arn arn:aws:iam::aws:policy/AmazonECS_FullAccess

# Create access key
aws iam create-access-key --user-name rowell-infra-deployment

# Save the Access Key ID and Secret Access Key from output!
```

---

## Step 6: Configure AWS CLI

Now configure AWS CLI with your credentials:

```bash
aws configure
```

You'll be prompted for:

1. **AWS Access Key ID**: Enter the Access Key ID you saved
   ```
   AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
   ```

2. **AWS Secret Access Key**: Enter the Secret Access Key you saved
   ```
   AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
   ```

3. **Default region name**: Enter your region
   ```
   Default region name [None]: us-east-1
   ```

4. **Default output format**: Choose `json`
   ```
   Default output format [None]: json
   ```

### Verify Configuration

```bash
# Test your credentials
aws sts get-caller-identity

# Should output something like:
# {
#     "UserId": "AIDAIOSFODNN7EXAMPLE",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/rowell-infra-deployment"
# }
```

If this works, you're all set! ✅

---

## Step 7: Test AWS Access

Run these commands to verify you have the right permissions:

```bash
# Test ECR access
aws ecr describe-repositories --region us-east-1

# Test ECS access
aws ecs list-clusters --region us-east-1

# Test EC2 access (for VPC/security groups)
aws ec2 describe-vpcs --region us-east-1

# Test CloudWatch Logs
aws logs describe-log-groups --region us-east-1
```

If all commands work without errors, you have the right permissions! ✅

---

## Step 8: Setup Billing Alerts (Important!)

Protect yourself from unexpected charges:

### Create Billing Alarm

1. **Go to CloudWatch**
   - https://console.aws.amazon.com/cloudwatch/
   - Or search "CloudWatch" in AWS Console

2. **Create Billing Alarm**
   - Click "Alarms" → "All alarms"
   - Click "Create alarm"
   - Click "Select metric"
   - Choose "Billing" → "EstimatedCharges"
   - Select your currency (USD)
   - Click "Select metric"
   - Set threshold (e.g., $50 if you have $100 in credits)
   - Set notification (create SNS topic if needed)
   - Click "Next" → "Create alarm"

3. **Create Budget**
   - Go to Billing → Budgets
   - Click "Create budget"
   - Choose "Cost budget"
   - Set amount (e.g., $80 if you have $100 credits)
   - Set alert thresholds
   - Click "Create budget"

---

## Step 9: Choose Your Deployment Method

You have two options:

### Option 1: AWS ECS (Elastic Container Service)
- **Best for**: Production, scalability, control
- **Complexity**: Medium
- **Cost**: ~$30-50/month

### Option 2: AWS Elastic Beanstalk
- **Best for**: Quick deployment, simplicity
- **Complexity**: Low
- **Cost**: ~$20-40/month

**Recommendation**: Start with **ECS** for better control and scalability.

---

## Step 10: Prepare Required Information

Before running deployment scripts, have ready:

### Database
- **Option A**: Use AWS RDS (we'll set it up)
- **Option B**: External database URL
  - Format: `postgresql+asyncpg://user:password@host:5432/dbname`

### Redis
- **Option A**: Use AWS ElastiCache (we'll set it up)
- **Option B**: External Redis URL
  - Format: `redis://host:6379/0`

### Hedera Credentials
- **Operator ID**: Get from https://portal.hedera.com → Developer → Testnet Access
  - Format: `0.0.1234567`
- **Operator Key**: Private key (starts with `302e`)
  - **Important**: Keep this secret!

### Secret Keys
- Generate strong random keys:
  ```bash
  # Generate secret key
  openssl rand -base64 32
  
  # Generate JWT secret
  openssl rand -base64 32
  ```

### CORS Origins
- Your frontend URL(s)
- Example: `https://your-frontend.com` or `http://localhost:3000` for development

---

## Quick Setup Checklist

- [ ] AWS account created/logged in
- [ ] AWS credits applied (if available)
- [ ] AWS CLI installed (`aws --version`)
- [ ] IAM user created (`rowell-infra-deployment`)
- [ ] Access keys created and saved
- [ ] AWS CLI configured (`aws configure`)
- [ ] Credentials verified (`aws sts get-caller-identity`)
- [ ] Billing alerts set up
- [ ] Region selected (us-east-1 recommended)
- [ ] Required information prepared (database, Redis, Hedera, secrets)

---

## Next Steps

Once AWS is set up:

1. **Run infrastructure setup:**
   ```bash
   ./scripts/setup-aws-resources.sh
   ```

2. **Deploy backend:**
   ```bash
   ./scripts/deploy-backend-aws.sh
   ```

3. **Set up database** (if using RDS):
   - See `BACKEND_AWS_DEPLOYMENT.md` Section: "Database Setup"

4. **Set up Redis** (if using ElastiCache):
   - See `BACKEND_AWS_DEPLOYMENT.md` Section: "Redis Setup"

---

## Troubleshooting

### Issue: "Unable to locate credentials"
```bash
# Re-run configuration
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_DEFAULT_REGION=us-east-1
```

### Issue: "Access Denied"
- Check IAM user has required policies attached
- Verify access key is for the correct user
- Ensure region is correct

### Issue: "Region not available"
- Choose a different region
- Some services may not be available in all regions

### Issue: "Credential expired"
- Generate new access keys in IAM Console
- Re-run `aws configure`

---

## Security Best Practices

1. ✅ **Never commit AWS credentials to git**
2. ✅ **Use IAM users, not root account**
3. ✅ **Rotate access keys regularly**
4. ✅ **Use least privilege (minimal permissions needed)**
5. ✅ **Enable MFA on root account**
6. ✅ **Set up billing alerts**
7. ✅ **Review CloudTrail logs periodically**

---

## Cost Management

### Free Tier Limits (First 12 Months)
- **EC2**: 750 hours/month (t2.micro)
- **RDS**: 750 hours/month (db.t2.micro)
- **ElastiCache**: Not included in free tier
- **ECR**: 500MB storage/month

### Estimated Costs (Beyond Free Tier)
- **ECS Fargate**: ~$15/month (1 task, 256 CPU, 512MB)
- **RDS**: ~$15/month (db.t3.micro)
- **ElastiCache**: ~$15/month (cache.t3.micro)
- **Total**: ~$45/month

**With AWS credits**, you should be well covered!

---

## Quick Reference Commands

```bash
# Check your AWS identity
aws sts get-caller-identity

# List all regions
aws ec2 describe-regions

# Check your account ID
aws sts get-caller-identity --query Account --output text

# View current configuration
aws configure list

# Test ECR access
aws ecr describe-repositories --region us-east-1

# Test ECS access
aws ecs list-clusters --region us-east-1
```

---

## Support Resources

- **AWS Documentation**: https://docs.aws.amazon.com
- **AWS Free Tier**: https://aws.amazon.com/free/
- **AWS Support**: https://console.aws.amazon.com/support/
- **AWS CLI Reference**: https://awscli.amazonaws.com/v2/documentation/

---

**Ready?** Now you can proceed to deployment:
```bash
./scripts/setup-aws-resources.sh
./scripts/deploy-backend-aws.sh
```

Good luck with your deployment! 🚀

