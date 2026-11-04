import re

from pages.base_page import BasePage


class VkIdPage(BasePage):
    _NEXT_BUTTON = "button:has-text('Далее')"

    def __init__(self, page):
        super().__init__(page)
        page.wait_for_url(re.compile(r"id\.vk\.ru"), wait_until="commit")

    def is_opened(self):
        return "id.vk.ru" in self.url

    def has_next_button(self):
        button = self.page.locator(self._NEXT_BUTTON).first
        button.wait_for(state="visible")  # экран VK ID дорисовывается асинхронно
        return button.is_visible()
