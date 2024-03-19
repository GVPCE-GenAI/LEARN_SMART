#!/bin/bash

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip

if aws --version > /dev/null 2>&1; then
    sudo ./aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update
    echo "AWS CLI is updated"
else
    echo "AWS CLI is not installed, Installing..."
    sudo ./aws/install
fi

sudo rm -r awscliv2.zip ./aws

# Specify the path to your .env file
ENV_FILE_PATH="Secrets/.env"

# Read AWS credentials from .env file
AWS_ACCESS_KEY_ID=$(grep AWS_ACCESS_KEY_ID $ENV_FILE_PATH | cut -d '=' -f2)
AWS_SECRET_ACCESS_KEY=$(grep AWS_SECRET_ACCESS_KEY $ENV_FILE_PATH | cut -d '=' -f2)

# Configure AWS CLI
aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
aws configure set default.region us-east-1  # Set your desired region here

cd app

pip3 install -r app/requirements.txt


# To know the current environment of python, use the command: which python