class BasePage:
    BASE_URL = "https://ok.ru"
    COOKIE_ACCEPT = "button.cb_accept"

    def __init__(self, page):
        self.page = page

    def open(self, path=""):
        self.page.goto(self.BASE_URL + path, wait_until="domcontentloaded")
        # ждём, пока страница навесит JS-обработчики: иначе клики теряются
        try:
            self.page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass  # реклама может держать сеть открытой бесконечно
        return self

    def accept_cookies(self):
        """Закрывает баннер про cookie, если он вылез."""
        button = self.page.locator(self.COOKIE_ACCEPT)
        if button.count():
            button.first.click()
        return self

    @property
    def url(self):
        return self.page.url
