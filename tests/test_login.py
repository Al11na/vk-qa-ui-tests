from pages.login_page import LoginPage

# только фейковые данные, реальных аккаунтов тут нет
FAKE_LOGIN = "autotest_fake_login@test.ru"
FAKE_PASSWORD = "WrongPassword123"


def test_login_form_is_displayed(page):
    assert LoginPage(page).open().is_displayed()


def test_wrong_credentials_show_error(page):
    login_page = LoginPage(page).open().login_as(FAKE_LOGIN, FAKE_PASSWORD)
    assert login_page.error_text() == "Неправильно указан логин и/или пароль"


def test_show_password_button_reveals_password(page):
    login_page = LoginPage(page).open().fill_credentials(FAKE_LOGIN, FAKE_PASSWORD).show_password()
    assert login_page.password_is_shown()


def test_forgot_password_opens_recovery_page(page):
    recovery_page = LoginPage(page).open().open_recovery()
    assert recovery_page.is_opened()
    assert recovery_page.has_support_link()


def test_registration_button_opens_vk_id_page(page):
    vk_id_page = LoginPage(page).open().open_registration()
    assert vk_id_page.is_opened()
    assert vk_id_page.has_next_button()
