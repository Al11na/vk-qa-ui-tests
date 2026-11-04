import os

import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage

pytestmark = pytest.mark.skipif(
    not (os.getenv("OK_LOGIN") and os.getenv("OK_PASSWORD")),
    reason="нет OK_LOGIN/OK_PASSWORD — заполни .env",
)


def test_login_opens_feed(page):
    """Логин с реальными кредами из .env открывает ленту."""
    home_page = LoginPage(page).open().login_as(os.environ["OK_LOGIN"], os.environ["OK_PASSWORD"])
    assert home_page.is_logged_in()
    assert home_page.posts_count() > 0


def test_feed_shows_posts(logged_page):
    assert HomePage(logged_page).open().posts_count() > 0


def test_own_profile_opens(logged_page):
    profile_page = HomePage(logged_page).open().open_own_profile()
    assert profile_page.is_opened()
    assert profile_page.has_settings_link()
