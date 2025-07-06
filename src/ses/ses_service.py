import boto3
from botocore.exceptions import ClientError

import config
from logger import log


class EmailService:
    def __init__(self):
        self.source = config.SES_SOURCE
        self.ses_client = boto3.client("ses", region_name=config.AWS_REGION)

    def send(self, username, email_type):
        try:
            response = self.ses_client.send_email(
                Destination={
                    "ToAddresses": [
                        username,
                    ],
                },
                # TODO tokenUrl is missing here
                Message={
                    "Body": {
                        "Html": {
                            "Charset": "UTF-8",
                            "Data": f"""<html>
                                <head></head>
                                <body>
                                  <h1>{email_type}</h1>
                                  <p>This email was sent with
                                    <a href='https://aws.amazon.com/ses/'>Amazon SES</a>
                                        using the
                                    <a href='https://aws.amazon.com/sdk-for-python/'>
                                      AWS SDK for Python (Boto)</a>.</p>
                                </body>
                                </html>""",
                        },
                        "Text": {
                            "Charset": "UTF-8",
                            "Data": (
                                f"{email_type}\r\n"
                                "This email was sent with Amazon SES using the "
                                "AWS SDK for Python (Boto)."
                            ),
                        },
                    },
                    "Subject": {
                        "Charset": "UTF-8",
                        "Data": f"{email_type}",
                    },
                },
                Source=f"No Reply <{config.SES_SOURCE}>",
                # If you are not using a configuration set, comment or delete the
                # following line
                ConfigurationSetName="ConfigSet",
            )

            log.debug(f"Sending ses message {response=}")

        except ClientError as e:
            log.error(f"Client error {e.response['Error']['Message']}")

            raise ClientError
        except Exception as e:
            log.error(f"Exception error {e}")

            raise Exception
        else:
            log.debug(f"Email sent! Message ID: {response['MessageId']}")

            log.debug("Successfully processed message")

            return response
