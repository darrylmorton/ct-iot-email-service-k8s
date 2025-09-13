import json
import time
from typing import Any

from botocore.exceptions import ClientError
from confluent_kafka import KafkaException, Consumer
from ses.ses_service import EmailService

import config
from logger import log


class EmailConsumer:
    def __init__(self):
        log.debug("initializing EmailConsumer...")

        self.consumer_config = {
            "bootstrap.servers": config.CONSUMER_BOOTSTRAP_SERVERS,
            "session.timeout.ms": config.CONSUMER_SESSION_TIMEOUT_MILLIS,
            "group.id": config.QUEUE_GROUP_ID,
            "auto.offset.reset": config.CONSUMER_AUTO_OFFSET_RESET,
            "enable.auto.offset.store": config.CONSUMER_ENABLE_AUTO_OFFSET_STORE,
        }
        self.consumer = Consumer(self.consumer_config)
        self.consumer.subscribe([config.QUEUE_TOPIC_NAME])

        self.email_service = EmailService()

        self.timeout_seconds = config.QUEUE_POLL_WAIT_SECONDS
        self.timeout = time.time() + self.timeout_seconds
        self.messages = []

    async def poll(self) -> None:
        log.debug("Polling for email messages...")

        await self.consume()

    def process_message(self, message_body: Any):
        log.debug("Processing email message...")

        timestamp = message_body.get("timestamp")
        email_type = message_body.get("email_type")
        username = message_body.get("username")
        first_name = message_body.get("first_name")
        token_url = message_body.get("token_url")
        token_url_hash = message_body.get("token_url_hash")

        if email_type in config.EMAIL_VERIFICATION_TYPES:
            try:
                response = self.email_service.send(
                    email_type, username, first_name, token_url, token_url_hash
                )

            except ClientError as e:
                log.error(f"Client error {e.response['Error']['Message']}")
            except Exception as e:
                log.error(f"Exception error {e}")
            else:
                log.debug(f"Email sent! Message ID: {response['MessageId']}")

                log.debug("Successfully processed message")

                return response
        else:
            return {"ResponseMetadata": {"HTTPStatusCode": 400}}

    # TODO type return missing
    async def consume(self):
        log.debug("Consuming email messages...")

        processed_message = {}

        try:
            while True:
                log.debug("consumer polling...")

                if time.time() > self.timeout:
                    log.debug(f"Task timed out after {self.timeout_seconds}")
                    break

                message = self.consumer.poll(config.QUEUE_POLL_WAIT_SECONDS)

                if message is None:
                    continue

                if message.error():
                    raise KafkaException(message.error())

                log.debug(
                    f"""{message.topic()=}, {message.partition()=}, 
                        {message.offset()=}, {str(message.key())=}"""
                )
                log.debug(f"{message.value()=}")

                message_body = json.loads(message.value())
                processed_message = self.process_message(message_body)

        except KafkaException as e:
            log.error(f"email_consumer error: {e}")

        finally:
            self.consumer.unsubscribe()
            self.consumer.close()

            return processed_message
