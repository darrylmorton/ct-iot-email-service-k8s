import boto3
from botocore.exceptions import ClientError

import config
from logger import log


class EmailService:
    def __init__(self):
        self.source = config.SES_SOURCE
        self.ses_client = boto3.client("ses", region_name=config.AWS_REGION)

    def send(self, email_type, username, first_name, token_url, token_url_hash) -> dict:
        try:
            response = self.ses_client.send_email(
                Destination={
                    "ToAddresses": [
                        username,
                    ],
                },
                Message={
                    "Body": {
                        "Html": {
                            "Charset": "UTF-8",
                            "Data": f"""<html>
                                <head></head>
                                <body>
                                  <h1>{email_type}</h1>
                                  <p>
                                    Dear {first_name},<br />
                                    Please confirm your account by clicking on the link below (expires in 1 hour):<br />
                                    <a href="{token_url}">{token_url_hash}</a>
                                  </p>
                                  <p>
                                    Thanks,<br />
                                    The Team
                                  </p>
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
