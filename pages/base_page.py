class BasePage:
    BASE_URL = "https://ok.ru"

    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto(self.BASE_URL, wait_until="domcontentloaded")
        # ждём, пока страница навесит JS-обработчики: иначе клики теряются
        try:
            self.page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass  # реклама может держать сеть открытой бесконечно
        return self

    @property
    def url(self):
        return self.page.url
