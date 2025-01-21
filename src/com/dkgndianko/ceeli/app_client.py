from typing import Dict, Tuple, List

from selenium.webdriver.common.by import By, ByType
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from com.dkgndianko.ceeli.base_client import BaseClient
from com.dkgndianko.ceeli.utils.param_types import Template
from com.dkgndianko.ceeli.utils.parameters import compile_template, format_template

DEFAULT_HOME_PATH = "/"
HOME_NAME = "home"

ElementLocator = Tuple[ByType, Template]


def parse_path(input_format: str) -> Template:
    without_leading_slash = input_format[1:] if input_format.startswith("/") else input_format
    return compile_template(without_leading_slash)


class AppClient(BaseClient):
    def __init__(self, base_url: str, browser: WebDriver = None, close_on_exit: bool = False):
        super().__init__(browser, close_on_exit)
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.sub_path_templates: Dict[str, Template] = {}
        self._named_element_locators: Dict[str, ElementLocator] = {}
        self.register_sub_path(HOME_NAME, DEFAULT_HOME_PATH)

    def register_sub_path(self, name: str, sub_path: str) -> None:
        """
        Register a sub path with a given name and a template. We can get the sub path by only giving the name and \
        parameters to fill in and format the template.\n
        ```
        client = AppClient("https://pythoncircle.com/", path)\n
        client.register_sub_path("post", "post/{post_id}/{slug:luma_neex}")\n
        client.go_to_path("post", post_id=775)
        ```
        :param name: The name of the sub path to use after when calling :func: `go_to_path`
        :param sub_path: The formatting of the sub path \
        e.g "/clients/{clientId}
        /export/{format:pdf} -> here 'pdf' is the default value of format that will be used if not given
        :return: None
        """
        sub_path = parse_path(sub_path)
        self.sub_path_templates[name] = sub_path

    def _get_url(self, name, **kwargs) -> str:
        try:
            sub_path_template = self.sub_path_templates[name]
        except KeyError:
            raise ValueError(f"no sub path with name ${name} registered. Use the {self.register_sub_path.__name__} \
            method to register")
        path = format_template(sub_path_template, **kwargs)
        return f"{self.base_url}/{path}"

    def home(self):
        """
        Go to the home page of the app. There is a default registered home path. It can be overridden using the method \
        `~register_sub_path(HOME_NAME, 'the_home_sub_url')`
        :return:
        """
        self.go_to_path(HOME_NAME)

    def go_to_path(self, name, **kwargs):
        """
        Go to a given sub path by just giving the already registered name and parameters to fill in the template
        :param name: The name of the registered sub path
        :param kwargs: key-word arguments to use to format the template
        :return: None
        """
        url = self._get_url(name, **kwargs)
        self.go_to(url)

    def __register_named_element_locator(self, name: str, locator_template: str, by: ByType):
        parsed_locator_template = compile_template(locator_template)
        self._named_element_locators[name] = (by, parsed_locator_template)

    def register_x_path_locator(self, name: str, x_path_template: str):
        """
        Registers a XPath locator template and give it a name. This name could be used later with the methods \
        :func:`~com.dkgndianko.ceeli.AppClient.find_element_by_locator_name` and \
        :func:`~com.dkgndianko.ceeli.AppClient.find_elements_by_locator_name`
        :param name: The name to register to
        :param x_path_template: The XPath locator template
        :return: None
        """
        self.__register_named_element_locator(name, x_path_template, By.XPATH)

    def register_css_selector(self, name: str, css_selector_template: str):
        self.__register_named_element_locator(name, css_selector_template, By.CSS_SELECTOR)

    def __get_locator_by_slug(self, slug: str, **kwargs) -> Tuple[str, ByType]:
        try:
            by, locator_def = self._named_element_locators[slug]
        except KeyError:
            raise ValueError(f"No named element registered with name '{slug}'.")
        return format_template(locator_def, **kwargs), by

    def find_element_by_locator_name(self, name: str, **kwargs) -> WebElement:
        locator, by = self.__get_locator_by_slug(name, **kwargs)
        return self._driver.find_element(by, locator)

    def find_elements_by_locator_name(self, name: str, **kwargs) -> List[WebElement]:
        locator, by = self.__get_locator_by_slug(name, **kwargs)
        return self._driver.find_elements(by, locator)

    def wait_for_locator(self, name: str, timeout: int, **kwargs) -> WebElement:
        locator, by = self.__get_locator_by_slug(name, **kwargs)
        return self.__wait_for(by, locator, timeout)
