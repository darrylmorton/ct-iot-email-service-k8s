from email_service.service import app
from tests.helper.routes_helper import RoutesHelper
from utils.app_util import AppUtil


class TestHealth:
    async def test_health(self):
        expected_result = {"message": "ok", "version": AppUtil.get_app_version()}

        response = await RoutesHelper.http_client(app, "/healthz")
        actual_result = response.json()

        assert response.status_code == 200
        assert actual_result == expected_result
