import tests.config as test_config
from tests.helper.email_helper import consumer_poll
from tests.helper.producer_helper import EmailProducer


class TestEmailConsumer:
    username = test_config.USERNAME

    async def test_email_consumer_email_sent(self, email_consumer):
        EmailProducer().produce(
            email_type=test_config.EMAIL_ACCOUNT_VERIFICATION_TYPE,
            username=self.username,
        )

        actual_result = await consumer_poll(
            _consumer=email_consumer, timeout_seconds=10
        )

        assert actual_result["ResponseMetadata"]["HTTPStatusCode"] == 200

    async def test_email_consumer_no_email_sent(self, email_consumer):
        EmailProducer().produce(
            email_type="invalid_email_type",
            username=self.username,
        )

        actual_result = await consumer_poll(
            _consumer=email_consumer, timeout_seconds=10
        )

        assert actual_result["ResponseMetadata"]["HTTPStatusCode"] == 400
