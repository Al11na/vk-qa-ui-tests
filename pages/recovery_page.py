import re

from pages.base_page import BasePage


class RecoveryPage(BasePage):
    _SUPPORT_LINK = "a:has-text('Обратиться в службу поддержки')"

    def __init__(self, page):
        super().__init__(page)
        # ok.ru держит документ «недогруженным» — ждём сам факт перехода
        page.wait_for_url(re.compile("anonymRecovery"), wait_until="commit")

    def is_opened(self):
        return "anonymRecovery" in self.url

    def has_support_link(self):
        link = self.page.locator(self._SUPPORT_LINK).first
        link.wait_for(state="visible")
        return link.is_visible()
