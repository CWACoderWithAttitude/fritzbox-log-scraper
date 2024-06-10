import os
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from scraper.tools import get_remote_ff

# sel_url = "http://selenium-hub:4444/wd/hub"
ID_PWD_FIELD = "uiPassInput"
ID_BTN_OK = "submitLoginBtn"
FRITZ_BOX_TITLE_AFTER_LOGIN = "FRITZ!Box 6591 Cable"


def select_username(driver: webdriver, username: str):
    url = os.environ["FRITZBOX_URL"]
    driver.get(url)
    # https://stackoverflow.com/questions/7867537/how-to-select-a-drop-down-menu-value-with-selenium-using-python
    select = Select(driver.find_element(By.ID, "uiViewUser"))

    return driver


def get_logs():
    driver = None
    try:
        driver = get_remote_ff()
        driver.get(os.environ["FRITZBOX_URL"])
        # https://stackoverflow.com/questions/7867537/how-to-select-a-drop-down-menu-value-with-selenium-using-python
        select = Select(driver.find_element(By.ID, "uiViewUser"))

        select.select_by_value(os.environ["FRITZBOX_USER"])
        # https://www.browserstack.com/guide/understanding-selenium-timeouts
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, ID_PWD_FIELD))
        )
        pwd_field = driver.find_element(By.ID, ID_PWD_FIELD)
        pwd_field.click()
        pwd_field.send_keys(os.environ["FRITZBOX_PASSWORD"])
    except:
        print("get_logs > Error1")
        if driver is not None:
            driver.quit()
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, ID_BTN_OK))
        )
        driver.find_element(By.ID, ID_BTN_OK).click()
    except:
        if driver is not None:
            driver.quit()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sys")))
        sys = driver.find_element(By.ID, "sys")
        sys.click()
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
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "logBox"))
        )
        logbox = driver.find_element(By.ID, "logBox")
        # print(f"logbox: {logbox}")
    except:
        print("get_logs > Error5")
        if driver is not None:
            driver.quit()
    return logbox


def Xtest_select_logon_user():
    driver = get_logs()
    # click 'Events' in sidemenu

    # now process log entries
    # log_entries = driver.find_elements(By.TAG_NAME, 'a')
    log_entries = driver.find_elements(By.CLASS_NAME, "print")
    num_entries = 10  # len(log_entries)
    assert num_entries != 0
    log_json = []
    for entry in log_entries:
        if len(log_json) > 10:
            exit
        else:
            print(f"test_select_logn_user: {len(log_json)}")
        num_entries = num_entries + 1
        line = entry.text
        dateMatch = re.search(r"\d{1,2}\.\d{1,2}\.\d{1,2}", line)
        date = line[dateMatch.start : dateMatch.end]
        time = re.search(r"\d{1,2}\:\d{1,2}\:\d{1,2}", line)
        msg = "msg"  # re.search('\"msg\"\>.*$', line) # not finished
        assert line != "blafaselblubb"
        log = {"date": date, "time": time, "msg": msg}
        print(log)
        log_json.append(log)
    assert len(log_json) + 1 == len(log_entries)
    driver.quit()
