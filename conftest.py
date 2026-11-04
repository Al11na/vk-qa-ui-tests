import pytest
from playwright.sync_api import sync_playwright

# без пометки Headless в UA: ok.ru отдаёт headless-браузерам битые страницы
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")


@pytest.fixture(scope="session")
def browser():
    # используем установленный Chrome, браузер Playwright не скачивается
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context(locale="ru-RU", user_agent=UA)
    yield context.new_page()
    context.close()
