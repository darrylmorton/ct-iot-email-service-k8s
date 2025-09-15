import hashlib
import socket

import tests.config as test_config
from logger import log


def create_config() -> dict:
    return {
        # User-specific properties that you must set
        "client.id": socket.gethostname(),
        # "bootstrap.servers": f"{config.QUEUE_PROTOCOL}:{config.QUEUE_PORTS}",
        "bootstrap.servers": f"{test_config.QUEUE_HOST}:9092",
        # Fixed properties
        "acks": "all",
    }


def create_token_url(token: str) -> str:
    """
    Creates a token URL for account confirmation.

    Args:
        token (str): The token to include in the URL.
    """

    return f"{test_config.USER_SERVICE_URL}/confirm-account?token={token}"


def create_hash_token_url(token_url: str) -> str:
    """
    Creates an SHA-256 hash of the token URL.

    Args:
        token_url (str): The token URL to hash.

    Returns:
        str: The SHA-256 hash of the token URL.
    """

    return hashlib.sha256(token_url.encode()).hexdigest()


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


def delivery_report(err, msg):
    """
    Reports the success or failure of a message delivery.

    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    """

    if err is not None:
        log.error("Delivery failed for User record {}: {}".format(msg.key(), err))
        return

    log.debug(
        "User record {} successfully produced to {} [{}] at offset {}".format(
            msg.key(), msg.topic(), msg.partition(), msg.offset()
        )
    )
