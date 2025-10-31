#!/bin/bash

# Rowell Infra - AWS Resources Setup Script
# This script creates all necessary AWS resources for backend deployment

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

AWS_REGION="${AWS_REGION:-us-east-1}"
PROJECT_NAME="rowell-infra"
SERVICE_NAME="${PROJECT_NAME}-api"
CLUSTER_NAME="${PROJECT_NAME}-cluster"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Rowell Infra - AWS Resources Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo -e "${RED}Error: AWS CLI not installed${NC}"
    exit 1
fi

# Check credentials
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text 2>/dev/null || echo "")
if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo -e "${RED}Error: AWS credentials not configured${NC}"
    exit 1
fi

echo -e "${GREEN}AWS Account: ${AWS_ACCOUNT_ID}${NC}"
echo -e "${GREEN}Region: ${AWS_REGION}${NC}"
echo ""

# 1. Create ECR Repository
echo -e "${YELLOW}[1/5] Creating ECR repository...${NC}"
if aws ecr describe-repositories --repository-names "$SERVICE_NAME" --region "$AWS_REGION" &> /dev/null; then
    echo -e "${GREEN}✓ ECR repository already exists${NC}"
else
    aws ecr create-repository \
        --repository-name "$SERVICE_NAME" \
        --region "$AWS_REGION" \
        --image-scanning-configuration scanOnPush=true
    echo -e "${GREEN}✓ ECR repository created${NC}"
fi
ECR_URI=$(aws ecr describe-repositories --repository-names "$SERVICE_NAME" --region "$AWS_REGION" --query 'repositories[0].repositoryUri' --output text)
echo "  ECR URI: $ECR_URI"
echo ""

# 2. Create ECS Cluster
echo -e "${YELLOW}[2/5] Creating ECS cluster...${NC}"
if aws ecs describe-clusters --clusters "$CLUSTER_NAME" --region "$AWS_REGION" --query 'clusters[0].status' --output text 2>/dev/null | grep -q ACTIVE; then
    echo -e "${GREEN}✓ ECS cluster already exists${NC}"
else
    aws ecs create-cluster --cluster-name "$CLUSTER_NAME" --region "$AWS_REGION"
    echo -e "${GREEN}✓ ECS cluster created${NC}"
fi
echo ""

# 3. Get or Create VPC and Networking
echo -e "${YELLOW}[3/5] Setting up networking...${NC}"
DEFAULT_VPC=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text --region "$AWS_REGION" 2>/dev/null)

if [ "$DEFAULT_VPC" == "None" ] || [ -z "$DEFAULT_VPC" ]; then
    echo "Creating VPC..."
    DEFAULT_VPC=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --region "$AWS_REGION" --query 'Vpc.VpcId' --output text)
    echo -e "${GREEN}✓ VPC created: $DEFAULT_VPC${NC}"
else
    echo -e "${GREEN}✓ Using existing VPC: $DEFAULT_VPC${NC}"
fi

# Get subnets
SUBNETS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$DEFAULT_VPC" --query 'Subnets[*].SubnetId' --output text --region "$AWS_REGION" 2>/dev/null)
if [ -z "$SUBNETS" ]; then
    echo "Creating subnets..."
    SUBNET1=$(aws ec2 create-subnet --vpc-id "$DEFAULT_VPC" --cidr-block 10.0.1.0/24 --availability-zone "${AWS_REGION}a" --region "$AWS_REGION" --query 'Subnet.SubnetId' --output text)
    SUBNET2=$(aws ec2 create-subnet --vpc-id "$DEFAULT_VPC" --cidr-block 10.0.2.0/24 --availability-zone "${AWS_REGION}b" --region "$AWS_REGION" --query 'Subnet.SubnetId' --output text)
    SUBNETS="$SUBNET1 $SUBNET2"
    echo -e "${GREEN}✓ Subnets created${NC}"
fi
echo "  VPC: $DEFAULT_VPC"
echo "  Subnets: $(echo $SUBNETS | tr ' ' ',')"
echo ""

# 4. Create Security Group
echo -e "${YELLOW}[4/5] Creating security group...${NC}"
SG_ID=$(aws ec2 describe-security-groups \
    --filters "Name=vpc-id,Values=$DEFAULT_VPC" "Name=group-name,Values=${PROJECT_NAME}-sg" \
    --query 'SecurityGroups[0].GroupId' \
    --output text \
    --region "$AWS_REGION" 2>/dev/null)

if [ "$SG_ID" == "None" ] || [ -z "$SG_ID" ]; then
    SG_ID=$(aws ec2 create-security-group \
        --group-name "${PROJECT_NAME}-sg" \
        --description "Security group for Rowell Infra" \
        --vpc-id "$DEFAULT_VPC" \
        --region "$AWS_REGION" \
        --query 'GroupId' \
        --output text)
    
    # Allow HTTP and HTTPS
    aws ec2 authorize-security-group-ingress \
        --group-id "$SG_ID" \
        --protocol tcp \
        --port 80 \
        --cidr 0.0.0.0/0 \
        --region "$AWS_REGION" 2>/dev/null || true
    
    aws ec2 authorize-security-group-ingress \
        --group-id "$SG_ID" \
        --protocol tcp \
        --port 443 \
        --cidr 0.0.0.0/0 \
        --region "$AWS_REGION" 2>/dev/null || true
    
    aws ec2 authorize-security-group-ingress \
        --group-id "$SG_ID" \
        --protocol tcp \
        --port 8000 \
        --cidr 0.0.0.0.0/0 \
        --region "$AWS_REGION" 2>/dev/null || true
    
    echo -e "${GREEN}✓ Security group created${NC}"
else
    echo -e "${GREEN}✓ Security group already exists${NC}"
fi
echo "  Security Group: $SG_ID"
echo ""

# 5. Create CloudWatch Log Group
echo -e "${YELLOW}[5/5] Creating CloudWatch log group...${NC}"
if aws logs describe-log-groups --log-group-name-prefix "/ecs/$SERVICE_NAME" --region "$AWS_REGION" --query 'logGroups[0].logGroupName' --output text 2>/dev/null | grep -q "/ecs"; then
    echo -e "${GREEN}✓ Log group already exists${NC}"
else
    aws logs create-log-group --log-group-name "/ecs/$SERVICE_NAME" --region "$AWS_REGION" 2>/dev/null || true
    echo -e "${GREEN}✓ Log group created${NC}"
fi
echo ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}AWS Resources Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Summary:"
echo "  ECR Repository: $ECR_URI"
echo "  ECS Cluster: $CLUSTER_NAME"
echo "  VPC: $DEFAULT_VPC"
echo "  Security Group: $SG_ID"
echo ""
echo "Next step: Run deploy-backend-aws.sh to deploy your application"
echo ""

