# ct-iot-email-service-k8s

## Description

[Diagrams](./docs/DIAGRAMS.md)

## Requirements
Python 3.11.9  
Poetry 1.7.1

## Install
```
poetry install
```

## Environment Variables
```
AWS_REGION=
SES_SOURCE=
SES_TARGET=
SENTRY_ENVIRONMENT=
SENTRY_DSN=
SENTRY_TRACES_SAMPLE_RATE=
SENTRY_PROFILES_SAMPLE_RATE=
SENTRY_SAMPLE_RATE=

SERVICE_NAME=
LOG_LEVEL=
ENVIRONMENT=
APP_HOST=
UVICORN_PORT=

CONSUMER_BOOTSTRAP_SERVERS=
CONSUMER_SESSION_TIMEOUT_MILLIS=
CONSUMER_AUTO_OFFSET_RESET=
CONSUMER_ENABLE_AUTO_OFFSET_STORE=

QUEUE_PROTOCOL=
QUEUE_HOST=
QUEUE_PORTS=
QUEUE_TIMEOUT_SECONDS=
QUEUE_ACKS=
QUEUE_POLL_WAIT_SECONDS=
QUEUE_TOPIC_NAME=
QUEUE_GROUP_ID=
EMAIL_ACCOUNT_VERIFICATION_TYPE=
```

## Run

### Development
```
docker compose -f docker-compose-local.yml up
make dev-server-start
```
Swagger docs: http://localhost:8003/docs

### Test
```
docker compose -f docker-compose-local.yml up
make test
```

### Helm | K8s 
```
# development
helm install email-service helm/email-service -f helm/email-service/local-values.yaml -n ct-iot
helm upgrade email-service helm/email-service -f helm/email-service/local-values.yaml -n ct-iot

k -n ct-iot port-forward svc/email-service 8003:9003 &

# production
helm install email-service helm/email-service -f helm/email-service/values.yaml -n ct-iot
helm upgrade email-service helm/email-service -f helm/email-service/values.yaml -n ct-iot

helm uninstall email-service -n ct-iot
```