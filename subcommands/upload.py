import boto3
import botocore.exceptions
import os
import sys

from providers.s3 import S3
from time import time

BUCKET = "hardcoded-bucket"


def upload(filepath, bucket=BUCKET):
    body = bytes_from_file_path(filepath)
    key = f"{int(time())}{file_extension(filepath)}"
    put_to_s3(key, body, bucket)


def file_extension(filepath):
    base, ext = os.path.splitext(
        os.path.basename(filepath))
    return ext


def bytes_from_file_path(filepath):
    try:
        with open(filepath, "rb") as fh:
            body = bytes(fh.read())
    except FileNotFoundError:
        sys.exit(f"Error: file {filepath} not found.")
    except PermissionError:
        sys.exit(f"Error: Permissions error reading {filepath}.")
    return body


def put_to_s3(key, body, bucket):
    try:
        s3_client = boto3.client('s3')
        s3 = S3(s3_client)
        s3.put_object(bucket=bucket, key=key, body=body)
    except botocore.exceptions.BotoCoreError as e:
        sys.exit("Error: unable to upload file.\n" + e.fmt)
    except botocore.exceptions.ClientError as e:
        sys.exit("Error: unable to upload file.\n" + e.response["Error"]["Message"])
    return key
