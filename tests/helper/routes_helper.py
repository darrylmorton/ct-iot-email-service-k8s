from httpx import AsyncClient, ASGITransport

from tests.config import APP_PORT


class RoutesHelper:
    TEST_URL = f"http://localhost:{APP_PORT}"

    @staticmethod
    async def http_client(app, path, token=None):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url=RoutesHelper.TEST_URL
        ) as ac:
            if token:
                ac.headers["authorization"] = f"Bearer {token}"

            return await ac.get(path)
