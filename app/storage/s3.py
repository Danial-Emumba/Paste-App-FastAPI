import boto3
import os
import logging
from fastapi import HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID", "default_access_key")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", "default_secret_key")
aws_default_region = os.getenv("AWS_DEFAULT_REGION", "default_region")
s3_bucket_name = os.getenv("S3_BUCKET_NAME", "default_bucket_name")

s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_default_region,
)


def save_to_s3(shortlink: str, paste_contents: str) -> None:
    logging.info(f"Saving paste contents to S3 with shortlink: {shortlink}")
    object_key = f"{shortlink}.txt"
    try:
        s3.put_object(Bucket=s3_bucket_name, Key=object_key, Body=paste_contents)
    except boto3.exceptions.S3UploadFailedError as e:
        logging.error(f"Failed to save paste to S3: {e}")
        raise HTTPException(status_code=500, detail="Failed to save paste to S3")


def get_paste_from_s3(shortlink: str) -> str:
    object_key = f"{shortlink}.txt"
    try:
        response = s3.get_object(Bucket=s3_bucket_name, Key=object_key)
        paste_contents = response["Body"].read().decode("utf-8")
        return paste_contents
    except s3.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="Paste not found")
    except Exception as e:
        logging.error(f"Failed to get paste from S3: {e}")
        raise HTTPException(status_code=500, detail="Failed to get paste from S3")


def delete_from_s3(shortlink: str) -> None:
    logging.info(f"Deleting paste with shortlink {shortlink} from S3")
    object_key = f"{shortlink}.txt"
    try:
        s3.delete_object(Bucket=s3_bucket_name, Key=object_key)
    except Exception as e:
        logging.error(f"Failed to delete paste from S3: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete paste from S3")
