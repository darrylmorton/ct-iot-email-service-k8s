import asyncio
import os
import boto3
from dotenv import load_dotenv
from moto import mock_aws

import pytest

from message_queue.email_consumer import EmailConsumer
import tests.config as test_config

load_dotenv(dotenv_path=".env.test")


@pytest.fixture
def aws_credentials():
    # Mocked AWS Credentials for moto
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_REGION"] = test_config.AWS_REGION


@pytest.fixture
def ses_client(aws_credentials):
    with mock_aws():
        conn = boto3.client("ses", region_name=test_config.AWS_REGION)
        conn.verify_email_identity(EmailAddress=test_config.SES_SOURCE)

        yield conn


@pytest.fixture
def email_consumer(ses_client):
    email_consumer = EmailConsumer()

    yield email_consumer


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()

    yield loop
    loop.close()
