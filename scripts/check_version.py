import argparse
from re import match
from packaging.version import Version, InvalidVersion

from logger import log
from utils.app_util import AppUtil


def main(arg_list: list[str] | None = None):
    log.info(f"main called with args: {arg_list}")

    app_version = AppUtil.get_app_version()

    parser = argparse.ArgumentParser(
        description="Check Application version is greater than the Release version."
    )
    parser.add_argument(
        "--latest-release-version",
        required=True,
        help="Latest Release version to check",
    )
    args = parser.parse_args(arg_list)

    try:
        latest_release_version = Version(args.latest_release_version)
    except InvalidVersion as error:
        error_message = (
            f"Invalid Release version {args.latest_release_version} does not match "
            f"semver format: {error}"
        )
        log.error(error_message)

        raise InvalidVersion(error_message)

    if not latest_release_version:
        error_message = f"Invalid Release version {latest_release_version}"
        log.error(error_message)

        raise ValueError(error_message)
    if not match(r"^[0-9]+\.[0-9]+\.[0-9]+$", f"{latest_release_version}"):
        error_message = (
            f"Invalid Release version {latest_release_version} does not match "
            f"semver format"
        )
        log.error(error_message)

        raise ValueError(error_message)
    if Version(app_version) <= Version(args.latest_release_version):
        error_message = (
            f"Invalid App version {app_version} is less than or equal "
            f"to the Release version {latest_release_version}"
        )
        log.error(error_message)

        raise ValueError(error_message)

    log.info(
        f"Valid Application version bump to {app_version} (greater than the "
        f"latest Release version {args.latest_release_version})."
    )


if __name__ == "__main__":
    main()
