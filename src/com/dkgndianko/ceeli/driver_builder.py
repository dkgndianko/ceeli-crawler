from pathlib import Path

from selenium.webdriver import Chrome, ChromeOptions


DEFAULT_DEBUGGER_HOST = "127.0.0.1"
DEFAULT_DEBUGGER_PORT = 9222

class WebDriverBuilder:

    def __init__(self):
        self.driver_options: ChromeOptions = ChromeOptions()

    def set_user_data_dir(self, user_data_dir: Path) -> "WebDriverBuilder":
        self.add_driver_option(f"user-data-dir={str(user_data_dir.absolute())}")
        return self

    def set_silent(self, silent: bool = False) -> "WebDriverBuilder":
        if silent:
            self.add_driver_option("--log-level=3")
        return self

    def set_headless(self, headless: bool = False) -> "WebDriverBuilder":
        if headless:
            self.add_driver_option("--headless")
        return self

    def set_detached(self, detached: bool = False) -> "WebDriverBuilder":
        if detached:
            self.add_driver_experimental_option("detach", True)
        return self

    def set_user_agent(self, user_agent) -> "WebDriverBuilder":
        self.add_driver_option(f"--user-agent={user_agent}")
        return self

    def set_incognito(self, incognito: bool = False) -> "WebDriverBuilder":
        if incognito:
            self.add_driver_option("--incognito")
        return self

    def set_remote_debugger(self, host: str = None, port: int = None) -> "WebDriverBuilder":
        self.driver_options.debugger_address = f"{host or DEFAULT_DEBUGGER_HOST}:{port or DEFAULT_DEBUGGER_PORT}"
        return self

    def expose_remote_debugging(self, host: str = None, port: int = None) -> "WebDriverBuilder":
        if host:
            self.add_driver_option(f"--remote-debugging-host={host}")
        if port:
            self.add_driver_option(f"--remote-debugging-port={port}")
        return self

    def add_driver_option(self, option: str):
        self.driver_options.add_argument(option)

    def add_driver_experimental_option(self, option_name: str, option_value):
        self.driver_options.add_experimental_option(option_name, option_value)

    def build(self) -> Chrome:
        return Chrome(options=self.driver_options)

