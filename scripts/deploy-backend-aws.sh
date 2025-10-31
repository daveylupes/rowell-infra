#!/bin/bash

# Rowell Infra - AWS Backend Deployment Script
# This script automates the deployment of the backend API to AWS ECS or Elastic Beanstalk

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
AWS_REGION="${AWS_REGION:-us-east-1}"
PROJECT_NAME="rowell-infra"
SERVICE_NAME="${PROJECT_NAME}-api"
CLUSTER_NAME="${PROJECT_NAME}-cluster"
ECR_REPO_NAME="${SERVICE_NAME}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Rowell Infra - AWS Backend Deployment${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}Error: AWS CLI is not installed${NC}"
        echo "Install it: https://aws.amazon.com/cli/"
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed${NC}"
        echo "Install it: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        echo -e "${RED}Error: AWS credentials not configured${NC}"
        echo "Run: aws configure"
        exit 1
    fi
    
    # Get AWS account ID
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    
    echo -e "${GREEN}✓ Prerequisites check passed${NC}"
    echo -e "  AWS Account ID: ${AWS_ACCOUNT_ID}"
    echo -e "  Region: ${AWS_REGION}"
    echo ""
}

# Ask deployment method
choose_deployment_method() {
    echo -e "${YELLOW}Choose deployment method:${NC}"
    echo "1) AWS ECS (Elastic Container Service) - Recommended"
    echo "2) AWS Elastic Beanstalk - Simpler"
    read -p "Enter choice [1 or 2]: " DEPLOYMENT_METHOD
    
    if [[ ! "$DEPLOYMENT_METHOD" =~ ^[12]$ ]]; then
        echo -e "${RED}Invalid choice${NC}"
        exit 1
    fi
    echo ""
}

# Deploy to ECS
deploy_to_ecs() {
    echo -e "${BLUE}Deploying to AWS ECS...${NC}"
    echo ""
    
    # Step 1: Create ECR repository if it doesn't exist
    echo -e "${YELLOW}Step 1: Setting up ECR repository...${NC}"
    if aws ecr describe-repositories --repository-names "$ECR_REPO_NAME" --region "$AWS_REGION" &> /dev/null; then
        echo -e "${GREEN}✓ ECR repository already exists${NC}"
    else
        echo "Creating ECR repository..."
        aws ecr create-repository \
            --repository-name "$ECR_REPO_NAME" \
            --region "$AWS_REGION" \
            --image-scanning-configuration scanOnPush=true
        echo -e "${GREEN}✓ ECR repository created${NC}"
    fi
    echo ""
    
    # Step 2: Build and push Docker image
    echo -e "${YELLOW}Step 2: Building and pushing Docker image...${NC}"
    cd api
    
    # Authenticate Docker to ECR
    echo "Authenticating Docker to ECR..."
    aws ecr get-login-password --region "$AWS_REGION" | \
        docker login --username AWS --password-stdin "$ECR_REGISTRY"
    
    # Build image
    echo "Building Docker image..."
    docker build -t "$ECR_REPO_NAME:latest" .
    
    # Tag and push
    echo "Tagging image..."
    docker tag "$ECR_REPO_NAME:latest" "$ECR_REGISTRY/$ECR_REPO_NAME:latest"
    docker tag "$ECR_REPO_NAME:latest" "$ECR_REGISTRY/$ECR_REPO_NAME:$(git rev-parse --short HEAD 2>/dev/null || echo 'latest')"
    
    echo "Pushing image to ECR..."
    docker push "$ECR_REGISTRY/$ECR_REPO_NAME:latest"
    docker push "$ECR_REGISTRY/$ECR_REPO_NAME:$(git rev-parse --short HEAD 2>/dev/null || echo 'latest')"
    
    echo -e "${GREEN}✓ Image pushed successfully${NC}"
    cd ..
    echo ""
    
    # Step 3: Create or update ECS cluster
    echo -e "${YELLOW}Step 3: Setting up ECS cluster...${NC}"
    if aws ecs describe-clusters --clusters "$CLUSTER_NAME" --region "$AWS_REGION" --query 'clusters[0].status' --output text 2>/dev/null | grep -q ACTIVE; then
        echo -e "${GREEN}✓ ECS cluster already exists${NC}"
    else
        echo "Creating ECS cluster..."
        aws ecs create-cluster --cluster-name "$CLUSTER_NAME" --region "$AWS_REGION"
        echo -e "${GREEN}✓ ECS cluster created${NC}"
    fi
    echo ""
    
    # Step 4: Check for existing task definition or create new
    echo -e "${YELLOW}Step 4: Setting up task definition...${NC}"
    read -p "Do you want to create a new task definition? [y/N]: " CREATE_TASK_DEF
    
    if [[ "$CREATE_TASK_DEF" =~ ^[Yy]$ ]]; then
        read -p "Enter database URL (postgresql://...): " DATABASE_URL
        read -p "Enter Redis URL (redis://...): " REDIS_URL
        read -p "Enter Hedera Testnet Operator ID (0.0.xxxxxxx): " HEDERA_OPERATOR_ID
        read -sp "Enter Hedera Testnet Operator Key: " HEDERA_OPERATOR_KEY
        echo ""
        read -sp "Enter Secret Key: " SECRET_KEY
        echo ""
        read -p "Enter CORS origins (comma-separated): " CORS_ORIGINS
        
        # Create task definition JSON
        cat > /tmp/task-definition.json <<EOF
{
  "family": "$SERVICE_NAME",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "$SERVICE_NAME",
      "image": "$ECR_REGISTRY/$ECR_REPO_NAME:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "DATABASE_URL", "value": "$DATABASE_URL"},
        {"name": "REDIS_URL", "value": "$REDIS_URL"},
        {"name": "HEDERA_TESTNET_OPERATOR_ID", "value": "$HEDERA_OPERATOR_ID"},
        {"name": "HEDERA_TESTNET_OPERATOR_KEY", "value": "$HEDERA_OPERATOR_KEY"},
        {"name": "SECRET_KEY", "value": "$SECRET_KEY"},
        {"name": "BACKEND_CORS_ORIGINS", "value": "[\\\"$CORS_ORIGINS\\\"]"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/$SERVICE_NAME",
          "awslogs-region": "$AWS_REGION",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
EOF
        
        # Create CloudWatch log group
        aws logs create-log-group --log-group-name "/ecs/$SERVICE_NAME" --region "$AWS_REGION" 2>/dev/null || true
        
        # Register task definition
        aws ecs register-task-definition \
            --cli-input-json file:///tmp/task-definition.json \
            --region "$AWS_REGION"
        
        echo -e "${GREEN}✓ Task definition created${NC}"
        rm /tmp/task-definition.json
    else
        echo "Using existing task definition..."
    fi
    echo ""
    
    # Step 5: Create or update ECS service
    echo -e "${YELLOW}Step 5: Creating/updating ECS service...${NC}"
    
    # Get default VPC and subnets
    DEFAULT_VPC=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text --region "$AWS_REGION")
    SUBNETS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$DEFAULT_VPC" --query 'Subnets[*].SubnetId' --output text --region "$AWS_REGION" | tr '\t' ',')
    SECURITY_GROUP=$(aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$DEFAULT_VPC" "Name=group-name,Values=default" --query 'SecurityGroups[0].GroupId' --output text --region "$AWS_REGION")
    
    if aws ecs describe-services --cluster "$CLUSTER_NAME" --services "$SERVICE_NAME" --region "$AWS_REGION" --query 'services[0].status' --output text 2>/dev/null | grep -q ACTIVE; then
        echo "Updating existing service..."
        aws ecs update-service \
            --cluster "$CLUSTER_NAME" \
            --service "$SERVICE_NAME" \
            --task-definition "$SERVICE_NAME" \
            --force-new-deployment \
            --region "$AWS_REGION" > /dev/null
        echo -e "${GREEN}✓ Service updated${NC}"
    else
        echo "Creating new service..."
        aws ecs create-service \
            --cluster "$CLUSTER_NAME" \
            --service-name "$SERVICE_NAME" \
            --task-definition "$SERVICE_NAME" \
            --desired-count 1 \
            --launch-type FARGATE \
            --network-configuration "awsvpcConfiguration={subnets=[$SUBNETS],securityGroups=[$SECURITY_GROUP],assignPublicIp=ENABLED}" \
            --region "$AWS_REGION" > /dev/null
        echo -e "${GREEN}✓ Service created${NC}"
    fi
    echo ""
    
    # Step 6: Wait for service to stabilize
    echo -e "${YELLOW}Step 6: Waiting for service to be stable...${NC}"
    echo "This may take a few minutes..."
    aws ecs wait services-stable \
        --cluster "$CLUSTER_NAME" \
        --services "$SERVICE_NAME" \
        --region "$AWS_REGION"
    echo -e "${GREEN}✓ Service is running${NC}"
    echo ""
    
    # Step 7: Get service status
    echo -e "${YELLOW}Step 7: Service Information${NC}"
    TASK_ARN=$(aws ecs list-tasks --cluster "$CLUSTER_NAME" --service-name "$SERVICE_NAME" --region "$AWS_REGION" --query 'taskArns[0]' --output text)
    
    if [ "$TASK_ARN" != "None" ] && [ -n "$TASK_ARN" ]; then
        PUBLIC_IP=$(aws ecs describe-tasks \
            --cluster "$CLUSTER_NAME" \
            --tasks "$TASK_ARN" \
            --region "$AWS_REGION" \
            --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value' \
            --output text | xargs -I {} aws ec2 describe-network-interfaces \
                --network-interface-ids {} \
                --region "$AWS_REGION" \
                --query 'NetworkInterfaces[0].Association.PublicIp' \
                --output text 2>/dev/null || echo "N/A")
        
        echo -e "${GREEN}✓ Deployment successful!${NC}"
        echo ""
        echo "Service Details:"
        echo "  Cluster: $CLUSTER_NAME"
        echo "  Service: $SERVICE_NAME"
        echo "  Public IP: $PUBLIC_IP"
        echo "  API URL: http://$PUBLIC_IP:8000"
        echo "  Health Check: http://$PUBLIC_IP:8000/health"
        echo "  Docs: http://$PUBLIC_IP:8000/docs"
    else
        echo -e "${YELLOW}Service is starting. Check AWS Console for IP address.${NC}"
    fi
    echo ""
    
    echo -e "${BLUE}View logs:${NC}"
    echo "  aws logs tail /ecs/$SERVICE_NAME --follow --region $AWS_REGION"
    echo ""
}

# Deploy to Elastic Beanstalk
deploy_to_eb() {
    echo -e "${BLUE}Deploying to AWS Elastic Beanstalk...${NC}"
    echo ""
    
    cd api
    
    # Check if EB is initialized
    if [ ! -d ".elasticbeanstalk" ]; then
        echo -e "${YELLOW}Initializing Elastic Beanstalk...${NC}"
        eb init -p docker -r "$AWS_REGION" "$SERVICE_NAME" --platform "Docker running on 64bit Amazon Linux 2"
    fi
    
    # Check if environment exists
    if eb list | grep -q "$SERVICE_NAME"; then
        echo -e "${GREEN}✓ Environment exists${NC}"
        read -p "Update existing environment? [Y/n]: " UPDATE_ENV
        if [[ ! "$UPDATE_ENV" =~ ^[Nn]$ ]]; then
            eb deploy "$SERVICE_NAME"
        fi
    else
        echo -e "${YELLOW}Creating new environment...${NC}"
        read -p "Enter database URL: " DATABASE_URL
        read -p "Enter Redis URL: " REDIS_URL
        read -p "Enter Hedera Testnet Operator ID: " HEDERA_OPERATOR_ID
        read -sp "Enter Hedera Testnet Operator Key: " HEDERA_OPERATOR_KEY
        echo ""
        read -sp "Enter Secret Key: " SECRET_KEY
        echo ""
        
        eb create "$SERVICE_NAME" \
            --platform "Docker running on 64bit Amazon Linux 2" \
            --instance-type t3.small \
            --envvars \
                "DATABASE_URL=$DATABASE_URL" \
                "REDIS_URL=$REDIS_URL" \
                "HEDERA_TESTNET_OPERATOR_ID=$HEDERA_OPERATOR_ID" \
                "HEDERA_TESTNET_OPERATOR_KEY=$HEDERA_OPERATOR_KEY" \
                "SECRET_KEY=$SECRET_KEY"
    fi
    
    # Get environment URL
    EB_URL=$(eb status "$SERVICE_NAME" | grep "CNAME" | awk '{print $2}')
    
    echo ""
    echo -e "${GREEN}✓ Deployment successful!${NC}"
    echo ""
    echo "Service Details:"
    echo "  Environment: $SERVICE_NAME"
    echo "  URL: http://$EB_URL"
    echo "  Health Check: http://$EB_URL/health"
    echo "  Docs: http://$EB_URL/docs"
    echo ""
    
    cd ..
}

# Main execution
main() {
    check_prerequisites
    choose_deployment_method
    
    if [ "$DEPLOYMENT_METHOD" == "1" ]; then
        deploy_to_ecs
    else
        deploy_to_eb
    fi
    
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Deployment Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
}

# Run main function
main

