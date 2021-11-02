from src.config.config import DATA_DIR, DVC_FILES
from src.config.logger_config import logger
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

import argparse
import os
import boto3

def upload_dvc_files():
    bucket = os.getenv('AWS_BUCKET')
    s3_client = boto3.client('s3')

    for file in DVC_FILES:
        path = str(Path(DATA_DIR, file))

        try:
            s3_client.upload_file(path, bucket, f'dvc_references/{file}')
            logger.info(f'Uploaded {file}')
        except:
            raise ValueError(f'Error uploading {file}')

def download_dvc_files():
    bucket = os.getenv('AWS_BUCKET')
    s3_client = boto3.client('s3')

    for file in DVC_FILES:
        path = str(Path(DATA_DIR, file))

        try:
            s3_client.download_file(bucket, f'dvc_references/{file}', path)
            logger.info(f'Downloaded {file}')
        except:
            raise ValueError(f'Error downloading {file}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--operation',
                    type=str,
                    required=True,
                    help='Operation to perform')
    args = parser.parse_args()

    if args.operation == 'upload':
        upload_dvc_files()
    elif args.operation == 'download':
        download_dvc_files()
    else:
        print('Operation must be {upload, download}')