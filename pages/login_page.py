from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.recovery_page import RecoveryPage
from pages.vk_id_page import VkIdPage


class LoginPage(BasePage):
    _EMAIL = "#field_email"
    _PASSWORD = "#field_password"
    _SUBMIT = "form:has(#field_email) button[type=submit]"
    _ERROR = "span[class*='LoginForm-module__error']"
    _SHOW_PASSWORD = "button:has-text('Показать пароль')"
    _FORGOT = "button:has-text('Не получается войти?')"
    _REGISTER = "button:has-text('Зарегистрироваться')"

    def is_displayed(self):
        self.page.locator(self._EMAIL).wait_for(state="visible")
        return self.page.locator(self._PASSWORD).is_visible()

    def fill_credentials(self, login, password):
        self.page.fill(self._EMAIL, login)
        self.page.fill(self._PASSWORD, password)
        return self

    def login_as(self, login, password):
        return self.fill_credentials(login, password).submit()

    def submit(self):
        self.page.click(self._SUBMIT)
        return self

    def error_text(self):
        error = self.page.locator(self._ERROR).first
        error.wait_for(state="visible")
        return error.text_content().strip()

    def show_password(self):
        # после fill() поле перерисовывается и клик «на опережение» теряется
        self.page.wait_for_timeout(500)
        self.page.click(self._SHOW_PASSWORD)
        expect(self.page.locator(self._PASSWORD)).to_have_attribute("type", "text")
        return self

    def password_is_shown(self):
        return self.page.get_attribute(self._PASSWORD, "type") == "text"

    def open_recovery(self):
        self.page.click(self._FORGOT)
        return RecoveryPage(self.page)

    def open_registration(self):
        self.page.click(self._REGISTER)
        return VkIdPage(self.page)
