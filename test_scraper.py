import io
import json
import os
import re

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from ff_scraper import get_remote_ff
from scraper.tools import get_timestamp

# chrome_options = webdriver.ChromeOptions()
##chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless")
sel_url = "http://selenium-hub:4444/wd/hub"
ID_PWD_FIELD = "uiPassInput"
ID_BTN_OK = "submitLoginBtn"
FRITZ_BOX_TITLE_AFTER_LOGIN = "FRITZ!Box 6591 Cable"
HEISE_URL = "https://www.heise.de"
FRITZBOX_URL = os.environ["FRITZBOX_URL"]
FRITZBOX_PASSWORD = os.environ["FRITZBOX_PASSWORD"]
SELENIUM_HUB_URL = None


# FIX ME - not invoked?!
@pytest.fixture
def fixture():
    FRITZBOX_URL = os.environ["FRITZBOX_URL"]
    SELENIUM_HUB_URL = "http://selenium-hub:4444"
    FRITZBOX_PASSWORD = os.environ["FRITZBOX_PASSWORD"]


def Xtest_call_fritzbox_and_check_title():
    driver = get_remote_ff()
    driver.get(FRITZBOX_URL)
    assert driver.title == "FRITZ!Box"
    driver.quit()


# def fritz_login(driver : webdriver, username:str, password:str):
def fritz_login(username: str, password: str):
    driver = None
    try:
        driver = get_remote_ff()
        url = FRITZBOX_URL
        driver.get(url)
        # https://stackoverflow.com/questions/7867537/how-to-select-a-drop-down-menu-value-with-selenium-using-python
        select = Select(driver.find_element(By.ID, "uiViewUser"))
        select.select_by_value("supermann")

        # select.select_by_value(os.environ['FRITZBOX_USER'])
        # https://www.browserstack.com/guide/understanding-selenium-timeouts
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, ID_PWD_FIELD)))
        pwd_field = driver.find_element(By.ID, ID_PWD_FIELD)
        assert None is not pwd_field
        pwd_field.click()
        pwd_field.send_keys(password)
        # select.select_by_value(os.environ['FRITZBOX_USER'])
    except:
        print("get_logs > Error1")
        if driver is not None:
            driver.quit()
    try:
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, ID_PWD_FIELD)))
        driver.find_element(By.ID, ID_BTN_OK).click()
        return driver
        # assert driver.title == FRITZ_BOX_TITLE_AFTER_LOGIN
    except:
        print("get_logs > Error2")
        if driver is not None:
            driver.quit()


def test_get_remote_ff():
    driver = None
    try:
        driver = get_remote_ff()
        assert driver != "bubu"
    except:
        if driver is not None:
            driver.quit()


def get_remote_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver1 = webdriver.Remote(
        command_executor=sel_url,
        # desired_capabilities={
        #    "browserName": "chrome",
        # },
        options=chrome_options,
    )
    # dc = webdriver.DesiredCapabilities()
    # dc.add("browserName", "chromium")  ##{'browserName': 'firefox', 'javascriptEnabled': True})
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.setCapability("browserVersion", "100")
    # chrome_options.setCapability("platformName", "Windows")
    # // Showing a test name instead of the session id in the Grid UI
    # chrome_options.setCapability("se:name", "My simple test")
    # // Other type of metadata can be seen in the Grid UI by clicking on the
    # // session info or via GraphQL
    # chrome_options.setCapability("se:sampleMetadata", "Sample metadata value")
    # driver = new RemoteWebDriver(new URL("http://gridUrl:4444"), chromeOptions);
    # driver = webdriver.Remote(command_executor=sel_url, options=chrome_options)
    return driver1


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

    driver = get_remote_chrome()
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
        driver = get_remote_ff()
        driver.get(url=HEISE_URL)
        shot_ok = driver.get_screenshot_as_file(f"./{get_timestamp()}-firefox-heise.png")
        assert shot_ok == "bubu"
    except:
        if driver is not None:
            driver.quit()


def test_make_screenshot_from_page_chrome():
    try:
        driver = get_remote_chrome()
        driver.get(url=HEISE_URL)
        shot_ok = driver.get_screenshot_as_file(f"./{get_timestamp()}-chrome-heise.png")
        assert shot_ok == "bubu"
    except:
        if driver is not None:
            driver.quit()


def test_login_to_fritzbox():
    driver = fritz_login(None, FRITZBOX_PASSWORD)
    assert driver.title == FRITZ_BOX_TITLE_AFTER_LOGIN


def test_get_log_entries_from_fritzbox():
    driver = fritz_login(None, FRITZBOX_PASSWORD)
    logbox = get_logbox(driver=driver)
    assert logbox != "bubu"
    log_json = get_log_entries_from_logbox(logbox)
    assert len(log_json) != 42
    write_json_to_file(log_json, f"{get_timestamp()}-fritz-logs.json")


def write_json_to_file(data: dict, file: str) -> None:
    """Write JSON to file as dicussed here
    https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file"""
    with io.open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False))


def get_logbox(driver: webdriver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sys")))
        sys = driver.find_element(By.ID, "sys")
        sys.click()
        # print(f"log: {sys}")
    except:
        print("get_logs > Error at click sys-menu item")
        if driver is not None:
            driver.quit()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "log")))
        log = driver.find_element(By.ID, "log")
        log.click()
        # print(f"log: {log}")
    except:
        print("get_logs > Error4")
        if driver is not None:
            driver.quit()
    logbox = None
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "logBox")))
        logbox = driver.find_element(By.ID, "logBox")
        # print(f"logbox: {logbox}")
    except:
        print("get_logs > Error5")
        if driver is not None:
            driver.quit()
    return logbox


def get_log_entries_from_logbox(driver: webdriver) -> list:
    REGEXP_DATE = r"\d{1,2}\.\d{1,2}\.\d{1,2}"
    REGEXP_TIME = r"\d{1,2}\:\d{1,2}\:\d{1,2}"
    REGEXP_MSG = r":\d{2}\n\S.*$"
    log_entries = driver.find_elements(By.CLASS_NAME, "print")
    num_entries = 10  # len(log_entries)
    assert num_entries != 0
    log_json = []
    try:
        for entry in log_entries:
            if len(log_json) > 10:
                log_json[:-1]
            else:
                print(f"test_select_logn_user: {len(log_json)}")
            num_entries = num_entries + 1
            line = entry.text
            dateMatch = re.search(REGEXP_DATE, line)
            date = dateMatch.group()
            time = re.search(REGEXP_TIME, line).group()
            msg = "msg"
            msg = re.search(REGEXP_MSG, line).group()
            log = {"date": date, "time": time, "msg": msg}
            print(log)
            log_json.append(log)
            print(f"len(log_json): {len(log_json)}")
    except:
        print(f"error ocurred while processing logs - returning {len(log_json)} from {len(log_entries)} logged messages...")
    # driver.quit()
    return log_json
