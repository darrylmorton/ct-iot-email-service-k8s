from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from fastapi import HTTPException
from jose import jwt, ExpiredSignatureError, JWTError

import tests.config as test_config
from logger import log


def create_token_expiry(
    _seconds=test_config.JWT_EXPIRY_SECONDS_CONFIRM_ACCOUNT,
) -> datetime:
    return datetime.now(tz=timezone.utc) + timedelta(seconds=_seconds)


def create_token(
    secret: str, data: dict, token_expiry: datetime = create_token_expiry()
):
    to_encode = data.copy()

    to_encode.update({"exp": token_expiry})
    encoded_jwt = jwt.encode(to_encode, secret, algorithm="HS256")

    return encoded_jwt


def create_token_expiry() -> datetime:
    return datetime.now(tz=timezone.utc) + timedelta(
        seconds=test_config.JWT_EXPIRY_SECONDS_CONFIRM_ACCOUNT
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token, test_config.JWT_SECRET_CONFIRM_ACCOUNT, algorithms=["HS256"]
        )

    except TypeError as error:
        log.debug(f"decode_token - type error {error}")

        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Token error")
    except ExpiredSignatureError as error:
        log.debug(f"decode_token - expired signature {error}")

        raise HTTPException(
            status_code=test_config.HTTP_STATUS_CODE_EXPIRED_TOKEN,
            detail="Expired token error",
        )
    except JWTError as error:
        log.debug(f"decode_token - invalid token {error}")

        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid JWT")
    except KeyError as error:
        log.debug(f"decode_token - invalid key {error}")

        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Invalid JWT payload"
        )


def encode_token(_username: str, _email_type: str):
    try:
        return jwt.encode(
            {
                "username": _username,
                "email_type": _email_type,
                "exp": create_token_expiry(),
            },
            test_config.JWT_SECRET_CONFIRM_ACCOUNT,
            algorithm="HS256",
        )
    except KeyError as error:
        log.debug(f"encode_token - key error {error}")

        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Token error")
    except TypeError as error:
        log.debug(f"encode_token - type error {error}")

        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Token error")
    except JWTError as error:
        log.debug(f"encode_token - jwt error {error}")

        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=error)
