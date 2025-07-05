# Cloud Secret Rotation

This project automates secure secret rotation and syncing between AWS Secrets Manager and GCP Secret Manager.

## 🌐 Features

- Read secrets from AWS Secrets Manager
- Push them into GCP Secret Manager
- Rotate secrets (DB credentials, tokens) securely
- Terraform setup for IAM on both clouds

## 📁 Structure

- `terraform/` – IAM setup for AWS and GCP
- `sync/`      – Python scripts to perform sync & rotation

## ⚙️ Tech Stack

- Python 3.10+
- Boto3, google-cloud-secret-manager
- Terraform
- GitHub Actions (optional)

## 🔒 Security

- No hardcoded credentials
- Uses environment variables or IAM roles
