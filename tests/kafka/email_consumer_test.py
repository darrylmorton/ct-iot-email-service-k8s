import tests.config as test_config
from tests.helper.kafka_helper import create_hash_token_url, create_token_url
from tests.helper.token_helper import create_token
from tests.helper.email_helper import consumer_poll
from tests.helper.producer_helper import EmailProducer


class TestEmailConsumer:
    token = create_token(
        secret=test_config.JWT_SECRET_CONFIRM_ACCOUNT,
        data={
            "username": test_config.USERNAME,
            "email_type": test_config.EMAIL_VERIFICATION_TYPES[0],
        },
    )
    token_url = create_token_url(token)
    hash_token_url = create_hash_token_url(token_url)

    async def test_email_consumer_email_sent(self, email_consumer):
        EmailProducer().produce(
            email_type=test_config.EMAIL_VERIFICATION_TYPES[0],
            username=test_config.USERNAME,
            first_name=test_config.FIRST_NAME,
            token_url=self.token_url,
            token_url_hash=self.hash_token_url,
        )

        actual_result = await consumer_poll(
            _consumer=email_consumer, timeout_seconds=10
        )

        assert actual_result["ResponseMetadata"]["HTTPStatusCode"] == 200

    async def test_email_consumer_no_email_sent(self, email_consumer):
        EmailProducer().produce(
            email_type="invalid_email_type",
            username=test_config.USERNAME,
            first_name=test_config.FIRST_NAME,
            token_url=self.token_url,
            token_url_hash=self.hash_token_url,
        )

        actual_result = await consumer_poll(
            _consumer=email_consumer, timeout_seconds=10
        )

        assert actual_result["ResponseMetadata"]["HTTPStatusCode"] == 400
