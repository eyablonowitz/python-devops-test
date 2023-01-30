import boto3
import botocore.exceptions
import os
import sys

from providers.s3 import S3
from time import time

BUCKET = "hardcoded-bucket"


def file_extension(filepath):
    base, ext = os.path.splitext(
        os.path.basename(filepath))
    return ext


def upload(filepath, s3_class=S3, bucket=BUCKET):
    try:
        with open(filepath, "rb") as fh:
            body = bytes(fh.read())
    except FileNotFoundError:
        sys.exit(f"Error: file {filepath} not found.")
    except PermissionError:
        sys.exit(f"Error: Permissions error reading {filepath}.")
    key = f"{int(time())}{file_extension(filepath)}"
    try:
        s3_client = boto3.client('s3')
        s3 = s3_class(s3_client)
        s3.put_object(bucket=bucket, key=key, body=body)
    except botocore.exceptions.BotoCoreError as e:
        sys.exit("Error: unable to upload file.\n" + e.fmt)
    except botocore.exceptions.ClientError as e:
        sys.exit("Error: unable to upload file.\n" + e.response["Error"]["Message"])
    return key
