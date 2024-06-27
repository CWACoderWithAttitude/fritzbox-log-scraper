import os
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

ID_PWD_FIELD = "uiPassInput"
ID_BTN_OK = "submitLoginBtn"
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


def get_logs_from_fritzbox() -> list:
    """Retrieve all logs from fritzbox as json array

    Returns:
        list[]: _description_
    """
    driver = fritz_login(FRITZBOX_URL, FRITZBOX_USER, FRITZBOX_PASSWORD)
    logbox = get_logbox(driver=driver)
    assert logbox != "bubu"
    log_json = get_log_entries_from_logbox(logbox)
    return log_json


def build_ff_options():
    ff_options = webdriver.FirefoxOptions()
    ff_options.add_argument("-headless")
    return ff_options


def get_remote_ff(selenum_grid_url: str):
    """Helper to get default firefox browser"""
    driver = webdriver.Remote(
        command_executor=selenum_grid_url,
        options=build_ff_options(),
    )
    return driver


def fritz_login(fritzbox_url: str, username: str, password: str):
    driver = None
    sel_url = "http://selenium-hub:4444/wd/hub"
    try:
        driver = get_remote_ff(selenum_grid_url=sel_url)
        driver.get(fritzbox_url)
        # https://stackoverflow.com/questions/7867537/how-to-select-a-drop-down-menu-value-with-selenium-using-python
        select = Select(driver.find_element(By.ID, "uiViewUser"))
        # select.select_by_value("supermann")
        select.select_by_value(username)

        # select.select_by_value(os.environ['FRITZBOX_USER'])
        # https://www.browserstack.com/guide/understanding-selenium-timeouts
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, ID_PWD_FIELD)))
        pwd_field = driver.find_element(By.ID, ID_PWD_FIELD)
        # assert None is not pwd_field
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
            log_json.append({"date": date, "time": time, "msg": msg})
            print(f"len(log_json): {len(log_json)}")
    except:
        print(f"error ocurred while processing logs - returning {len(log_json)} from {len(log_entries)} logged messages...")
    # driver.quit()
    return log_json


def get_remote_chrome(selenum_grid_url: str):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver1 = webdriver.Remote(
        command_executor=selenum_grid_url,
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
