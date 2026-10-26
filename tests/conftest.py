import os

import pytest
import requests


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        pytest.fail(
            f"Переменная окружения {name} не задана: укажи, против чего гонять тесты"
        )
    return value


@pytest.fixture(scope="session")
def base_url() -> str:
    """Адрес тестируемого стенда"""
    return _require_env("BASE_URL")


@pytest.fixture(scope="session")
def app_version() -> str:
    """Адрес тестируемого стенда"""
    return _require_env("EXPECTED_VERSION")


@pytest.fixture(scope="session")
def app_env() -> str:
    """Адрес тестируемого стенда"""
    return _require_env("EXPECTED_ENV")


@pytest.fixture(scope="session")
def auth_headers(base_url: str) -> dict[str, str]:
    """Вход в тестовую учётку стенда: POST /auth/test-login есть только на dev и test."""
    response = requests.post(f"{base_url}/api/v1/auth/test-login", timeout=5)
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['token']}"}
