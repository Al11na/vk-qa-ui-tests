from pages.base_page import BasePage
from pages.profile_page import ProfilePage


class HomePage(BasePage):
    """Главная страница залогиненного пользователя (лента)."""

    _OWN_PROFILE = "a.ui_navigation_user_block_link"
    _POST = "[data-feed-id]"

    def wait_ready(self):
        # ссылка «свой профиль» в шапке есть только у залогиненных
        self.page.locator(self._OWN_PROFILE).first.wait_for(state="visible")
        self.accept_cookies()
        return self

    def open(self):
        super().open()
        return self.wait_ready()

    def is_logged_in(self):
        return self.page.locator(self._OWN_PROFILE).count() > 0

    def posts_count(self):
        return self.page.locator(self._POST).count()

    def open_own_profile(self):
        self.page.locator(self._OWN_PROFILE).first.click()
        return ProfilePage(self.page)
