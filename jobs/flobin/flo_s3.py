# coding=utf-8
from boto3 import client
from os import environ


class S3Base(object):
    """Store in-house recurring S3 functionality."""

    def __init__(self, **kwargs):
        """Initialize default attributes.

        :param aws_access_key_id: str specifying the AWS access key
        :param aws_secret_access_key: str specifying the AWS secret key
        :param region_name: str specifying the AWS region
        """
        self.env = environ['APP_ENV']
        self.bucket = 'flosports-data-warehouse-sources' if self.env == 'prod' else 'datawarehouse-staging-sources'
        self.raw_bucket = 'flosports-data-warehouse-raw-sources' if self.env == 'prod' else 'datawarehouse-staging-raw-sources'
        self.client = client(
            's3',
            aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY'],
            region_name='us-west-2'
        )
