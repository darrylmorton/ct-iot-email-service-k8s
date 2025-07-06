import json
import time

from confluent_kafka import KafkaException

from kafka.email_consumer import EmailConsumer
from logger import log
import tests.config as test_config


async def consumer_poll(_consumer: EmailConsumer, timeout_seconds=0):
    timeout = time.time() + timeout_seconds
    processed_message = {}

    try:
        log.debug("email_consuming....")

        while True:
            log.debug("consumer polling...")

            if time.time() > timeout:
                log.debug(f"Task timed out after {timeout_seconds}")
                break

            message = _consumer.consumer.poll(test_config.QUEUE_POLL_WAIT_SECONDS)

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
            processed_message = _consumer.process_message(message_body)

    except KafkaException as e:
        log.error(f"email_consumer error: {e}")

    finally:
        _consumer.consumer.unsubscribe()
        _consumer.consumer.close()

        return processed_message


def create_email_message(
    timestamp: str,
    email_type: str,
    username: str,
    token: str,
) -> dict:
    return dict(
        email_type=email_type,
        username=username,
        timestamp=timestamp,
        token=token,
    )
