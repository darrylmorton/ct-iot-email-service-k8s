# The builder image, used to build the virtual environment
FROM python:3.11.9-slim as builder

RUN pip install --upgrade pip && pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN ls -la /usr/local/bin

WORKDIR /ct-iot-email-service

COPY pyproject.toml poetry.lock requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt


# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11.9-slim as runtime

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ENV VIRTUAL_ENV=/ct-iot-email-service/venv \
    PATH="/usr/local/bin:/ct-iot-email-service/venv/bin:$PATH"

WORKDIR /ct-iot-email-service

ENV PYTHONPATH src/

COPY . .

RUN ls -la

CMD ["uvicorn", "email_service.service:app", "--host", "0.0.0.0"]

EXPOSE 8003 9090
