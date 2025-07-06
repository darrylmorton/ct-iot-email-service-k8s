import os
import uvicorn

import config
from logger import log


def main():
    log.info(f"Starting {config.SERVICE_NAME}...")

    try:
        cores = os.cpu_count()

        if cores is None:
            calculated_workers = 3
        else:
            calculated_workers = 2 * cores + 1

        log.info(f"Running uvicorn with multiple workers {calculated_workers}")

        uvicorn.run(
            app="email_service.service.app",
            workers=calculated_workers,
            log_config=None,
        )
    except Exception as error:
        log.error(f"Error with uvicorn {error}")
        raise Exception


if __name__ == "__main__":
    main()
