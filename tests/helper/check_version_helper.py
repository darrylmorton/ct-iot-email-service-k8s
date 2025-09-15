from utils.app_util import AppUtil


def bump_version(version: str = AppUtil.get_app_version(), part: str = "patch") -> str:
    """
    Bumps the specified part of a semver version string.
    part: 'major', 'minor', or 'patch'
    """
    major, minor, patch = map(int, version.split("."))

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError("part must be 'major', 'minor', or 'patch'")

    return f"{major}.{minor}.{patch}"


def downgrade_version(
    version: str = AppUtil.get_app_version(), part: str = "patch"
) -> str:
    """
    Downgrades the specified part of a semver version string.
    part: 'major', 'minor', or 'patch'
    """
    major, minor, patch = map(int, version.split("."))

    if part == "major":
        if major == 0:
            raise ValueError("major version cannot be less than 0")
        major -= 1
        minor = 0
        patch = 0
    elif part == "minor":
        if minor == 0:
            raise ValueError("minor version cannot be less than 0")
        minor -= 1
        patch = 0
    elif part == "patch":
        if patch == 0:
            raise ValueError("patch version cannot be less than 0")
        patch -= 1
    else:
        raise ValueError("part must be 'major', 'minor', or 'patch'")

    return f"{major}.{minor}.{patch}"
