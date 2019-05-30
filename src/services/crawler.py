from collections import namedtuple
from pathlib import Path
from time import sleep

from selenium.common.exceptions import NoSuchElementException

from services.common import CACHE_ROOT
from services.exceptions import (
    BookContainerWaitError,
    LibraryIframeWaitError,
    LoginElementsWaitError,
)
from lib.crypt import AESCipher
from lib.driver_builder import DriverBuilder
from lib.helper import current_date_str, make_now
from lib.logger import logger
from models.master_models_generated import User

BASE_URL = "https://read.amazon.co.jp/"
AmazonAccount = namedtuple("AmazonAccount", "email password")


def pick_amazon_account(user: User):
    cipher = AESCipher(user.email)
    plain_password = cipher.decrypt(user.password)
    return AmazonAccount(user.email, plain_password)


def login(driver, account: AmazonAccount):
    c = 0
    while True:
        sleep(1)
        c += 1
        if c > 30:
            raise LoginElementsWaitError

        uid = driver.find_element_by_name("email")
        password = driver.find_element_by_name("password")
        if uid and password:
            break

    uid.send_keys(account.email)
    password.send_keys(account.password)
    driver.find_element_by_id("signInSubmit").click()
    logger.info("login")


def pick_iframe(driver):
    c = 0
    while True:
        sleep(3)
        c += 1
        if c > 5:
            raise LibraryIframeWaitError

        try:
            iframe = driver.find_element_by_css_selector("#KindleLibraryIFrame")
        except NoSuchElementException:
            continue
        if iframe:
            return iframe


def wait_book_container(driver):
    c = 0
    while True:
        sleep(3)
        c += 1
        if c > 5:
            raise BookContainerWaitError

        try:
            wrapper = driver.find_element_by_css_selector("#titles_inner_wrapper")
        except NoSuchElementException:
            continue
        containers = wrapper.find_elements_by_css_selector(".book_container")
        if len(containers) > 0:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            break


def save_cache(driver, root: Path):
    now = make_now()
    nowstr = "%04d-%02d-%02d-%02d-%02d-%02d-%05d" % (
        now.year,
        now.month,
        now.day,
        now.hour,
        now.minute,
        now.second,
        now.microsecond,
    )
    cache_file = root / f"{nowstr}.html"
    with cache_file.open("w") as f:
        f.write(driver.page_source)


def crawl(user: User):
    account: AmazonAccount = pick_amazon_account(user)

    user_cache_root: Path = CACHE_ROOT / str(user.id)
    current_cache_root: Path = user_cache_root / current_date_str()
    for root in [user_cache_root, current_cache_root]:
        if not root.exists():
            root.mkdir()

    driver_builder = DriverBuilder()
    driver = driver_builder.get_driver(headless=False)
    try:
        driver.get(BASE_URL)
        login(driver, account=account)
        iframe = pick_iframe(driver)
        driver.switch_to_frame(iframe)
        wait_book_container(driver)
        cache_file = current_cache_root / "cache.html"
        with cache_file.open("w") as f:
            f.write(driver.page_source)

    except Exception as e:
        logger.error(type(e))
        logger.error(e)

    finally:
        driver.close()
        driver.quit()
        logger.info("close & quit driver")
