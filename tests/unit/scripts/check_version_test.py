import pytest
from packaging.version import InvalidVersion

from scripts.check_version import main
from tests.helper.check_version_helper import downgrade_version, bump_version
from utils.app_util import AppUtil


class TestCheckVersionScript:
    _app_version = AppUtil.get_app_version()
    _release_version = downgrade_version(part="major")
    _release_version_bump = bump_version()

    def test_get_app_version_matches_release(self):
        with pytest.raises(ValueError) as exc_info:
            main(["--latest-release-version", self._app_version])

        assert exc_info.value.args[0] == (
            f"Invalid App version {self._app_version} is less than or equal to the "
            f"Release version {self._app_version}"
        )

    def test_get_app_version_less_than_release(self):
        with pytest.raises(ValueError) as exc_info:
            main(["--latest-release-version", self._release_version_bump])

        assert exc_info.value.args[0] == (
            f"Invalid App version {self._app_version} is less than or equal to the "
            f"Release version {self._release_version_bump}"
        )

    def test_release_version_invalid_semver_number(self):
        with pytest.raises(ValueError) as exc_info:
            main(["--latest-release-version", "2"])

        assert (
            exc_info.value.args[0]
            == "Invalid Release version 2 does not match semver format"
        )

    def test_release_version_invalid_semver_letter(self):
        with pytest.raises(InvalidVersion) as exc_info:
            main(["--latest-release-version", "a"])

        assert (
            exc_info.value.args[0]
            == "Invalid Release version a does not match semver format: "
            "Invalid version: 'a'"
        )

    def test_get_app_version_greater_than_release(self):
        main(["--latest-release-version", self._release_version])
