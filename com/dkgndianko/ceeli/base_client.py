from pathlib import Path
from typing import Optional, List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class BaseClient:

    def __init__(
            self,
            user_data_dir: Path,
            silent: Optional[bool] = False,
            headless: Optional[bool] = False,
            detached: Optional[bool] = False
    ):
        self._browser_started = False
        self.driver_options = webdriver.ChromeOptions()
        self.add_driver_option(f"user-data-dir={str(user_data_dir.absolute())}")
        if silent:
            self.add_driver_option("--log-level=3")
        if headless:
            self.add_driver_option("--headless")
        if detached:
            self.add_driver_experimental_option("detach", True)
        # self.add_driver_option("--user-agent=Ceeli")
        self.add_driver_option("--incognito")
        self.browser = webdriver.Chrome(options=self.driver_options)
        self._browser_started = True

    def add_driver_option(self, option: str):
        if self._browser_started:
            raise ValueError("cannot add an option when the browser has started")
        self.driver_options.add_argument(option)

    def add_driver_experimental_option(self, option_name: str, option_value):
        if self._browser_started:
            raise ValueError("cannot add an option when the browser has started")
        self.driver_options.add_experimental_option(option_name, option_value)

    def go_to(self, url: str) -> None:
        self.browser.get(url)

    def save_screenshot(self, destination: str) -> bool:
        return self.browser.save_screenshot(destination)

    def get_screenshot_bytes(self) -> bytes:
        return self.browser.get_screenshot_as_png()

    def find_elements_by_x_path(self, xpath: str) -> List[WebElement]:
        return self.browser.find_elements(By.XPATH, xpath)

    def find_elements_by_name(self, name: str) -> List[WebElement]:
        return self.browser.find_elements(By.NAME, name)

    def find_elements_by_tag_name(self, tag_name: str) -> List[WebElement]:
        return self.browser.find_elements(By.TAG_NAME, tag_name)

    def find_elements_by_class_name(self, class_name: str) -> List[WebElement]:
        return self.browser.find_elements(By.CLASS_NAME, class_name)

    def find_elements_by_css_selector(self, css_selector: str) -> List[WebElement]:
        return self.browser.find_elements(By.CSS_SELECTOR, css_selector)

    def find_element_by_id(self, _id: str) -> WebElement:
        return self.browser.find_element(By.ID, _id)

    def test(self):
        print(str(self.driver_options.to_capabilities()))
        self.browser.get('https://www.google.com')
        print(self.browser.title)
