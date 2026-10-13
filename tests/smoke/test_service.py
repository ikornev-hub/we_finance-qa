import pytest
import requests

pytestmark = pytest.mark.smoke


def test_health_is_ok(base_url):
    response = requests.get(f"{base_url}/health", timeout=5)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_get_version(base_url, app_version, app_env):
    response = requests.get(f"{base_url}/version", timeout=5)
    assert response.status_code == 200
    assert response.json()["version"] == app_version
    assert response.json()["env"] == app_env
