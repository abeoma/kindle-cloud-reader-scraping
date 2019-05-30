from selenium.webdriver import Chrome
from selenium.webdriver.chrome import webdriver as chrome_webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from lib.logger import logger


class DriverBuilder:
    def get_driver(self, download_location="./", headless=False):

        driver = self._get_chrome_driver(download_location, headless)

        driver.set_window_size(1400, 1000)

        return driver

    def _get_chrome_driver(self, download_location, headless):
        chrome_options = chrome_webdriver.Options()
        if download_location:
            prefs = {
                "download.default_directory": download_location,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": False,
                "safebrowsing.disable_download_protection": True,
            }

            chrome_options.add_experimental_option("prefs", prefs)

        if headless:
            chrome_options.add_argument("--headless")

        driver_path = "/usr/local/bin/chromedriver"

        driver = Chrome(executable_path=driver_path, chrome_options=chrome_options)

        if headless:
            self.enable_download_in_headless_chrome(driver, download_location)

        return driver

    def enable_download_in_headless_chrome(self, driver, download_dir):
        driver.command_executor._commands["send_command"] = (
            "POST",
            "/session/$sessionId/chromium/send_command",
        )
        params = {
            "cmd": "Page.setDownloadBehavior",
            "params": {"behavior": "allow", "downloadPath": download_dir},
        }
        command_result = driver.execute("send_command", params)
        # logger.info("response from browser:")
        # for key in command_result:
        #     logger.info(f"result: {key}:{str(command_result[key])}")


def _find_elem_with_wait(driver, selector: tuple) -> WebElement:
    return WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(selector)
    )


def find_elem_by_classname_with_wait(driver, classname: str) -> WebElement:
    return _find_elem_with_wait(driver, selector=(By.CLASS_NAME, classname))


def find_elem_by_xpath_with_wait(driver, xpath: str) -> WebElement:
    return _find_elem_with_wait(driver, selector=(By.XPATH, xpath))
