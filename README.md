# 🔐 Cloud Secret Rotation

This project automates **secure secret rotation and syncing** between **AWS Secrets Manager** and **GCP Secret Manager**, helping maintain cross-cloud security hygiene and compliance.

---

## 🌐 Features

- 🔁 Sync secrets from **AWS Secrets Manager → GCP Secret Manager**
- 🔄 **Rotate secrets** (e.g., DB credentials, API keys)
- ⚙️ Terraform setup for least-privilege IAM roles on both clouds
- 📦 Configurable mapping for multiple secrets
- 💡 Future-ready for GitHub Actions or cron-based automation

---

## 📁 Folder Structure

```text
cloud-secret-rotation/
├── terraform/          # IAM setup for AWS and GCP
│   ├── aws_iam.tf
│   ├── gcp_iam.tf
│   └── variables.tf
├── sync/               # One-way sync from AWS to GCP
│   ├── aws_to_gcp.py
│   └── secrets_map.yaml
├── rotate/             # Secret rotation logic (currently AWS password rotation)
│   └── rotate_password.py
├── .gitignore
├── requirements.txt
└── README.md
```
# ⚙️ Tech Stack
- Python 3.10+
- boto3 – AWS SDK for Python
- google-cloud-secret-manager
- PyYAML – to parse secret maps
- Terraform – for IAM provisioning
- GitHub Actions (optional) – to automate rotation/sync jobs

# 🔒 Security Practices
- ✅ No hardcoded credentials or secrets in code
- ✅ Uses environment variables and IAM roles
- ✅ .gitignore includes .tfstate, *.json, and sensitive paths
- ✅ Secrets encrypted in-transit and at rest using cloud-native KMS

# 🚀 Usage
# 1. 🔁 Sync AWS → GCP
```
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export GCP_PROJECT_ID=your-gcp-project-id
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/gcp-key.json"

python sync/aws_to_gcp.py
```
# 2. 🔄 Rotate Secret in AWS and Sync to GCP
```python rotate/rotate_password.py```

# 🧠 Future Enhancements
 - GCP → AWS sync support
 - GitHub Actions scheduler
 - Slack/Discord notifications
 - Integration with Vault/KMS for stronger encryption
   
# 🛠️ Contributing
### Pull requests are welcome. For major changes, please open an issue first.

# 📄 License
## MIT
