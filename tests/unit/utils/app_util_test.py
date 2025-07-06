from utils.app_util import AppUtil


class TestAppUtil:
    _id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"

    async def test_get_app_version(self):
        actual_result = AppUtil.get_app_version()

        assert actual_result == "1.0.0"
