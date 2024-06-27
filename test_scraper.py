import os

import pytest

from scraper.logscraper import get_remote_ff, get_remote_chrome, fritz_login, get_log_entries_from_logbox, get_logbox
from scraper.tools import get_timestamp, write_json_to_file

sel_url = "http://selenium-hub:4444/wd/hub"
ID_PWD_FIELD = "uiPassInput"
ID_BTN_OK = "submitLoginBtn"
FRITZ_BOX_TITLE_AFTER_LOGIN = "FRITZ!Box 6591 Cable"
HEISE_URL = "https://www.heise.de"
FRITZBOX_URL = os.environ["FRITZBOX_URL"]
FRITZBOX_USER = os.environ["FRITZBOX_USER"]
FRITZBOX_PASSWORD = os.environ["FRITZBOX_PASSWORD"]
WHAT_BROWSER = os.environ["WHAT_BROWSER"]
SELENIUM_HUB_URL = "http://selenium-hub:4444"

# def fritz_login(driver : webdriver, username:str, password:str):


@pytest.fixture
def before():
    print("Before")


def test_get_remote_ff():
    driver = None
    capa = {}
    try:
        driver = get_remote_ff(SELENIUM_HUB_URL)
        assert driver.capabilities == "bubu"
        # capa = driver.capabilities
    except:
        if driver is not None:
            driver.quit()
    # assert capa["browserName"] == "Operas"


def test_get_remote_chrome():
    driver = get_remote_chrome()
    assert driver == "bubu"


def test_get_page_chrome():
    title = None

    driver = get_remote_chrome()
    driver.get(url=HEISE_URL)
    title = driver.title
    if driver is not None:
        driver.quit()

    assert title == "heise online - IT-News, Nachrichten und Hintergründe | heise online"


def test_get_selenium_hub_page_chrome():
    title = None

    driver = get_remote_chrome(sel_url=sel_url)
    driver.get(url=SELENIUM_HUB_URL)
    title = driver.title
    if driver is not None:
        driver.quit()

    assert title == "Selenium Grid"


def test_get_page_firefox():
    title = None

    driver = get_remote_ff()
    driver.get(url=HEISE_URL)
    title = driver.title
    if driver is not None:
        driver.quit()

    assert title == "heise online - IT-News, Nachrichten und Hintergründe | heise online"


def test_make_screenshot_from_page_firefox():
    try:
        driver = get_remote_ff(selenum_grid_url=sel_url)
        driver.get(url=WHAT_BROWSER)
        shot_ok = driver.get_screenshot_as_file(f"./{get_timestamp()}-firefox-what_browser.png")
        assert shot_ok == "bubu"
    except:
        if driver is not None:
            driver.quit()


def test_make_screenshot_from_page_chrome():
    try:
        driver = get_remote_chrome(selenum_grid_url=sel_url)
        driver.get(url=WHAT_BROWSER)
        shot_ok = driver.get_screenshot_as_file(f"./{get_timestamp()}-chrome-what_browser.png")
        assert shot_ok == "bubu"
    except:
        if driver is not None:
            driver.quit()


def test_login_to_fritzbox():
    driver = fritz_login(None, FRITZBOX_PASSWORD)
    assert driver.title == FRITZ_BOX_TITLE_AFTER_LOGIN


def test_get_log_entries_from_fritzbox():
    driver = fritz_login(FRITZBOX_URL, FRITZBOX_USER, FRITZBOX_PASSWORD)
    logbox = get_logbox(driver=driver)
    assert logbox != "bubu"
    log_json = get_log_entries_from_logbox(logbox)
    assert len(log_json) >= 1
    write_json_to_file(log_json, f"{get_timestamp()}-fritz-logs.json")
