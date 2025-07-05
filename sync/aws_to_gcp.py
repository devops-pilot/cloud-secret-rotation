import boto3
import yaml
import os
from google.cloud import secretmanager_v1
from google.api_core.exceptions import NotFound

# Load AWS client
aws_client = boto3.client('secretsmanager')

# Load GCP client
gcp_client = secretmanager_v1.SecretManagerServiceClient()
gcp_project_id = os.environ.get("GCP_PROJECT_ID")

if not gcp_project_id:
    raise EnvironmentError("GCP_PROJECT_ID environment variable not set")

# Load the secret map
with open("sync/secrets_map.yaml", 'r') as file:
    mapping = yaml.safe_load(file)

for secret in mapping['secrets']:
    aws_name = secret['aws_name']
    gcp_name = secret['gcp_name']
    print(f"\n🔄 Syncing {aws_name} → {gcp_name}")

    # Get secret from AWS
    try:
        aws_response = aws_client.get_secret_value(SecretId=aws_name)
        secret_value = aws_response['SecretString']
        print("✅ Fetched from AWS")
    except Exception as e:
        print(f"❌ Failed to get AWS secret: {e}")
        continue

    # Build GCP secret path
    parent = f"projects/{gcp_project_id}"
    secret_path = f"{parent}/secrets/{gcp_name}"

    # Check if GCP secret exists
    try:
        gcp_client.get_secret(name=secret_path)
    except NotFound:
        print("📦 GCP secret does not exist. Creating it.")
        gcp_client.create_secret(
            parent=parent,
            secret_id=gcp_name,
            secret={
                "replication": {
                    "automatic": {}
                }
            }
        )

    # Add new version with latest value
    gcp_client.add_secret_version(
        parent=secret_path,
        payload={"data": secret_value.encode("UTF-8")}
    )
    print("✅ Synced to GCP Secret Manager")
