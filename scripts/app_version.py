from utils.app_util import AppUtil


def get_app_version():
    app_version = AppUtil.get_app_version()

    print(app_version)


if __name__ == "__main__":
    get_app_version()
