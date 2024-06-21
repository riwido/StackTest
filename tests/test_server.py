import importlib

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

import stacktest.server


@pytest.mark.parametrize(
    ["dev_mode"],
    [
        pytest.param("", id="normal environment"),
        pytest.param("1", id="dev environment"),
    ],
)
class TestServer:
    @pytest.fixture
    def client(self, app):
        with TestClient(app) as test_client:
            yield test_client

    @pytest.fixture
    def app(self, dev_mode, monkeypatch):
        monkeypatch.setenv("STACKTEST_DEBUG", dev_mode)
        importlib.reload(stacktest.server)
        yield stacktest.server.app

    def test_root(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_data(self, client):
        response = client.get("/data")
        assert response.status_code == 200

    def test_404(self, client):
        response = client.get("/fhqwhgads.asdf")
        assert response.status_code == 404

    def test_ws(self, client):
        with client.websocket_connect("/ws") as websocket:
            assert websocket.receive_text()

    async def test_disconnect(self, app):
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            r = await client.get("/")
