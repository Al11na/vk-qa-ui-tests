import re

from pages.base_page import BasePage


class ProfilePage(BasePage):
    """Страница профиля пользователя."""

    _SETTINGS = "a:has-text('Настройки'):visible"

    def __init__(self, page):
        super().__init__(page)
        page.wait_for_url(re.compile(r"/profile/\d+"), wait_until="commit")

    def is_opened(self):
        return re.search(r"/profile/\d+", self.url) is not None

    def has_settings_link(self):
        # «Настройки» видны только в своём профиле
        link = self.page.locator(self._SETTINGS).first
        link.wait_for(state="visible")
        return link.is_visible()
