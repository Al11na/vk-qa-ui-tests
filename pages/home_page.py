from pages.base_page import BasePage
from pages.profile_page import ProfilePage


class HomePage(BasePage):
    """Главная страница залогиненного пользователя (лента)."""

    # ссылка на свой профиль — в DOM есть только у залогиненных
    _OWN_PROFILE_LINK = "a[hrefattrs='st.cmd=userPage']"
    _POST = "[data-feed-id]"

    def wait_ready(self):
        self.page.locator(self._OWN_PROFILE_LINK).first.wait_for(state="attached")
        self.accept_cookies()
        return self

    def open(self):
        super().open()
        return self.wait_ready()

    def is_logged_in(self):
        return self.page.locator(self._OWN_PROFILE_LINK).count() > 0

    def posts_count(self):
        return self.page.locator(self._POST).count()

    def open_own_profile(self):
        href = self.page.locator(self._OWN_PROFILE_LINK).first.get_attribute("href")
        self.page.locator(f"a[href='{href}']:visible").first.click()
        return ProfilePage(self.page)
