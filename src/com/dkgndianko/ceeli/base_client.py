from typing import List

from selenium.webdriver.common.by import By, ByType
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from com.dkgndianko.ceeli.driver_builder import WebDriverBuilder


class BaseClient:

    def __init__(
            self,
            browser: WebDriver = None,
            close_on_exit: bool = False
    ):
        self._driver = browser or WebDriverBuilder().set_silent(True).set_incognito(True).set_detached(True).build()
        self.close_on_exit = close_on_exit

    def go_to(self, url: str) -> None:
        self._driver.get(url)

    def save_screenshot(self, destination: str) -> bool:
        return self._driver.save_screenshot(destination)

    def get_screenshot_bytes(self) -> bytes:
        return self._driver.get_screenshot_as_png()

    def find_elements_by_x_path(self, xpath: str) -> List[WebElement]:
        return self._driver.find_elements(By.XPATH, xpath)

    def find_elements_by_name(self, name: str) -> List[WebElement]:
        return self._driver.find_elements(By.NAME, name)

    def find_elements_by_tag_name(self, tag_name: str) -> List[WebElement]:
        return self._driver.find_elements(By.TAG_NAME, tag_name)

    def find_elements_by_class_name(self, class_name: str) -> List[WebElement]:
        return self._driver.find_elements(By.CLASS_NAME, class_name)

    def find_elements_by_css_selector(self, css_selector: str) -> List[WebElement]:
        return self._driver.find_elements(By.CSS_SELECTOR, css_selector)

    def find_element_by_id(self, _id: str) -> WebElement:
        return self._driver.find_element(By.ID, _id)

    def wait_for_x_path(self, x_path: str, timeout: int) -> WebElement:
        return self.__wait_for(By.XPATH, x_path, timeout)

    def wait_for_name(self, name: str, timeout: int) -> WebElement:
        return self.__wait_for(By.NAME, name, timeout)

    def wait_for_tag_name(self, tag_name: str, timeout: int) -> WebElement:
        return self.__wait_for(By.TAG_NAME, tag_name, timeout)

    def wait_for_class_name(self, class_name: str, timeout: int) -> WebElement:
        return self.__wait_for(By.CLASS_NAME, class_name, timeout)

    def wait_for_css_selector(self, css_selector: str, timeout: int) -> WebElement:
        return self.__wait_for(By.CSS_SELECTOR, css_selector, timeout)

    def wait_for_id(self, _id: str, timeout: int) -> WebElement:
        return self.__wait_for(By.ID, _id, timeout)

    def __wait_for(self, by: ByType, value: str, timeout: int) -> WebElement:
        wait = WebDriverWait(self._driver, timeout)
        try:
            return wait.until(EC.presence_of_element_located((by, value)))
        except:
            return None

    def close(self):
        self._driver.close()

    def quit(self):
        self._driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._driver and self.close_on_exit:
            self._driver.close()

    def test(self):
        self._driver.start_tab_mirroring()
        self._driver.get('https://www.google.com')
        print(self._driver.title)
