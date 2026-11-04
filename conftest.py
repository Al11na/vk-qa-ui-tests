import os
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from pages.login_page import LoginPage

# без пометки Headless в UA: ok.ru отдаёт headless-браузерам битые страницы
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")


def _load_env():
    """Читает логин/пароль из .env — файл лежит рядом и не попадает в git."""
    env_file = Path(__file__).with_name(".env")
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


_load_env()
OK_LOGIN = os.getenv("OK_LOGIN", "")
OK_PASSWORD = os.getenv("OK_PASSWORD", "")


@pytest.fixture(scope="session")
def browser():
    # используем установленный Chrome, браузер Playwright не скачивается
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        yield browser
        browser.close()


@pytest.fixture
def context(browser):
    context = browser.new_context(locale="ru-RU", user_agent=UA)
    yield context
    context.close()


@pytest.fixture
def page(context):
    return context.new_page()


@pytest.fixture(scope="session")
def auth_state(browser):
    """Логинится один раз и отдаёт cookies, чтобы не логиниться в каждом тесте."""
    if not OK_LOGIN or not OK_PASSWORD:
        pytest.skip("нет OK_LOGIN/OK_PASSWORD — заполни .env")
    context = browser.new_context(locale="ru-RU", user_agent=UA)
    LoginPage(context.new_page()).open().login_as(OK_LOGIN, OK_PASSWORD)
    state = context.storage_state()
    context.close()
    return state


@pytest.fixture
def logged_page(browser, auth_state):
    context = browser.new_context(locale="ru-RU", user_agent=UA, storage_state=auth_state)
    yield context.new_page()
    context.close()
