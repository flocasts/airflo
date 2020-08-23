# coding=utf-8
from boto3 import client
from os import environ


class SSMBase(object):
    """Store in-house recurring SSM functionality."""

    def __init__(self, **kwargs):
        """Initialize default attributes.

        :param aws_access_key_id: str specifying the AWS access key
        :param aws_secret_access_key: str specifying the AWS secret key
        :param region_name: str specifying the AWS region
        """
        self.env = environ['APP_ENV']
        self.client = client(
            'ssm',
            aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY'],
            region_name='us-west-2'
        )

    def get_param(self, param_name, decrypt=True):
        """Read and parse secure values from AWS's SSM service.

        :param param_name: str of param key
        :return: str value stored for param_name
        """
        _response = self.client.get_parameter(
            Name=param_name,
            WithDecryption=decrypt
        )
        response = _response.get('Parameter').get('Value')
        if response.startswith(('{', '[')):
            response = eval(response)
        return response

    def get_snowflake_creds(self):
        """Retrieve and return spark args."""
        db_user = self.get_param(f'{self.env}-azathoth-snowflake-username')
        db_pass = self.get_param(f'{self.env}-azathoth-snowflake-password')

        return {
            'sfURL': 'ck46883.snowflakecomputing.com',
            'sfWarehouse': 'LOADING',
            'sfDatabase': 'ANALYTICS' if self.env == 'prod' else 'RAW_STAGING',
            'sfAccount': 'ck46883',
            'sfUser': db_user,
            'sfPassword': db_pass,
            'keep_column_case': 'off'
        }
