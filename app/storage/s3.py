import boto3
from fastapi import HTTPException
from app.config.settings import Settings

settings = Settings()

aws_access_key_id = settings.AWS_ACCESS_KEY_ID
aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
aws_default_region = settings.AWS_REGION
s3_bucket_name = settings.AWS_S3_BUCKET_NAME

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_default_region)

def save_to_s3(shortlink: str, paste_contents: str):
    print(f"Saving paste contents to S3 with shortlink: {shortlink}")
    object_key = f'{shortlink}.txt'
    try:
        s3.put_object(Bucket=s3_bucket_name, Key=object_key, Body=paste_contents)
    except Exception as e:
        print(f"Failed to save paste to S3: {e}")

def get_paste_from_s3(shortlink: str) -> str:
    object_key = f'{shortlink}.txt'
    try:
        response = s3.get_object(Bucket=s3_bucket_name, Key=object_key)
        paste_contents = response['Body'].read().decode('utf-8')
        return paste_contents
    except s3.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="Paste not found")
    except Exception as e:
        print(f"Failed to get paste from S3: {e}")

def delete_from_s3(shortlink: str):
    print(f"Deleting paste with shortlink {shortlink} from S3")
    object_key = f'{shortlink}.txt'
    try:
        s3.delete_object(Bucket=s3_bucket_name, Key=object_key)
    except Exception as e:
        print(f"Failed to delete paste from S3: {e}")
