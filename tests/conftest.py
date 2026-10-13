import os

import pytest


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
