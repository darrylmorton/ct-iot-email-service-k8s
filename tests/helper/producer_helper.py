import asyncio
import calendar
import json
import time
import uuid
from datetime import datetime, timezone
from threading import Thread
from confluent_kafka import Producer, KafkaException

from logger import log
import tests.config as test_config
from tests.helper.email_helper import create_email_message
from tests.helper.kafka_helper import create_config
from tests.helper.token_helper import encode_token


class EmailProducer:
    def __init__(self, loop=None):
        log.debug("initializing EmailProducer...")

        producer_config = create_config()
        self._producer = Producer(producer_config)

        self._loop = loop or asyncio.get_event_loop()
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            self._producer.poll(test_config.QUEUE_POLL_WAIT_SECONDS)

    def _close(self):
        self._cancelled = True
        self._poll_thread.join()

    def produce(self, email_type: str, username: str):
        """
        An awaitable produce method.
        """
        try:
            result = self._loop.create_future()

            def _ack(err, msg):
                if err:
                    log.error(f"Kafka produce ack {err}")

                    self._loop.call_soon_threadsafe(
                        result.set_exception, KafkaException(err)
                    )
                else:
                    self._loop.call_soon_threadsafe(result.set_result, msg)

            message = create_email_message(
                username=username,
                email_type=email_type,
                timestamp=datetime.now(tz=timezone.utc).isoformat(),
                token=encode_token(username, email_type),
            )

            self._producer.produce(
                topic=test_config.QUEUE_TOPIC_NAME,
                key=str(uuid.uuid4()),
                value=json.dumps(message),
                timestamp=calendar.timegm(time.gmtime()),
                on_delivery=_ack,
            )
            self._producer.flush()
            log.debug(f"Kafka produced {message=} and flushed")

        except KafkaException as err:
            log.error(f"Kafka produce {err}")
        finally:
            self._close()
            log.debug("Kafka closed producer")
