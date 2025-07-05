import boto3
import os
import random
import string
from google.cloud import secretmanager_v1
from google.api_core.exceptions import NotFound

# AWS + GCP setup
aws_client = boto3.client("secretsmanager")
gcp_client = secretmanager_v1.SecretManagerServiceClient()
gcp_project_id = os.environ.get("GCP_PROJECT_ID")

if not gcp_project_id:
    raise EnvironmentError("GCP_PROJECT_ID environment variable not set")

# --- CONFIGURATION ---

# This could be pulled from a config file later
ROTATION_MAP = [
    {
        "aws_name": "app/db-password",
        "gcp_name": "db-password"
    }
]

# --- UTILS ---

def generate_password(length=20):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))


# --- MAIN ROTATION LOGIC ---

for item in ROTATION_MAP:
    aws_name = item["aws_name"]
    gcp_name = item["gcp_name"]

    print(f"\n🔄 Rotating secret: {aws_name} → {gcp_name}")

    # 1. Generate new password
    new_password = generate_password()
    print(f"🔐 Generated new password.")

    # 2. Update AWS secret
    try:
        aws_client.put_secret_value(
            SecretId=aws_name,
            SecretString=new_password
        )
        print(f"✅ Updated AWS Secret: {aws_name}")
    except Exception as e:
        print(f"❌ Failed to update AWS Secret: {e}")
        continue

    # 3. Push to GCP
    secret_path = f"projects/{gcp_project_id}/secrets/{gcp_name}"

    try:
        gcp_client.get_secret(name=secret_path)
    except NotFound:
        print("📦 GCP secret does not exist. Creating it.")
        gcp_client.create_secret(
            parent=f"projects/{gcp_project_id}",
            secret_id=gcp_name,
            secret={"replication": {"automatic": {}}}
        )

    try:
        gcp_client.add_secret_version(
            parent=secret_path,
            payload={"data": new_password.encode("UTF-8")}
        )
        print(f"✅ Updated GCP Secret: {gcp_name}")
    except Exception as e:
        print(f"❌ Failed to update GCP Secret: {e}")
