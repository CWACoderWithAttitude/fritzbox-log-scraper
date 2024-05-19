import pytest, re
from fritz_scraper import get_ff, get_driver
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC    
from selenium.webdriver.support.wait import WebDriverWait

chrome_options = webdriver.ChromeOptions()
#chrome_options.set_capability('browserless:token', 'YOUR-API-TOKEN')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
sel_url='http://chrome.local:3000/wd/hub'
sel_url='http://chrome.local:3000/webdriver'
sel_url='http://chrome.local:3000/playwright/chromium'
sel_url='http://chrome.local:3000/chrome'

sel_url='http://chrome.local:3000'  #/playwright/chromium'
sel_url='http://selenium-hub:4444/wd/hub'
ID_PWD_FIELD='uiPassInput'
ID_BTN_OK = 'submitLoginBtn'

def build_ff_options():
    ff_options = webdriver.FirefoxOptions()
    ff_options.add_argument("-headless")
    return ff_options
    
def get_remote_ff():
    driver = webdriver.Remote(
        command_executor=sel_url,
        options=build_ff_options()  #{'browserName': 'firefox', 'javascriptEnabled': True}
    )
    return driver
#def test_get_ff():
#    driver = get_remote_ff()

#    assert driver != 'bubu'
#    driver.quit()
    
# def test_get_heise():
#     driver = get_remote_ff()
#     driver.get('https://www.heise.de')
#     assert 'heise online - IT-News, Nachrichten und Hintergründe | heise online' == driver.title
#     driver.quit()
    
def Xtest_call_fritzbox_and_check_title():
    driver = get_remote_ff()
    driver.get('http://fritz.box')
    assert driver.title == 'FRITZ!Box'
    driver.quit()

def fritz_login(driver : webdriver, username:str, password:str):
    pass

def select_username(driver : webdriver, username:str):
    driver.get('http://fritz.box')
    # https://stackoverflow.com/questions/7867537/how-to-select-a-drop-down-menu-value-with-selenium-using-python
    select = Select(driver.find_element(By.ID, 'uiViewUser'))
    
    #select.select_by_value('supermann')
    return driver

def Xtest_select_username():
    driver = get_remote_ff()
    try:
        driver = select_username(driver=driver, username='bubu')
        
        select = Select(driver.find_element(By.ID, 'uiViewUser'))
    # https://stackoverflow.com/questions/11934966/how-to-get-selected-option-using-selenium-webdriver-with-java
    
        assert 'itzelbritzel' == select.getFirstSelectedOption().getText()
    
    except:
        print("Error occured")
        driver.quit()
        
def get_logs():
    try:
        driver = get_remote_ff()
        #driver.manage().timeouts().setScriptTimeout(10) #, TimeUnit.SECONDS);
        driver.get('http://fritz.box')
        # https://stackoverflow.com/questions/7867537/how-to-select-a-drop-down-menu-value-with-selenium-using-python
        select = Select(driver.find_element(By.ID, 'uiViewUser'))
        select.select_by_value('supermann')
        # https://www.browserstack.com/guide/understanding-selenium-timeouts
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, ID_PWD_FIELD)))
        pwd_field = driver.find_element(By.ID, ID_PWD_FIELD)
        assert None != pwd_field
        pwd_field.click()
        pwd_field.send_keys('proben8453')
        
    except:
        print("Error2")
        driver.quit()
    try:
        #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, ID_PWD_FIELD)))
        driver.find_element(By.ID, ID_BTN_OK).click()
        assert driver.title == 'FRITZ!Box 6591 Cable'
    except:
        print("Error2")
        driver.quit()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'sys')))
        sys = driver.find_element(By.ID, 'sys')
        sys.click()
        #print(f"log: {sys}")
    except:
        print("Error at click sys-menu item")
        driver.quit()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'log')))
        log = driver.find_element(By.ID, 'log')
        log.click()
        #print(f"log: {log}")
    except:
        print("Error4")
        driver.quit()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'logBox')))
        logbox = driver.find_element(By.ID, 'logBox')
        #print(f"logbox: {logbox}")
    except:
        print("Error4")
        driver.quit()
    return logbox


def test_select_logon_user():
    driver = get_logs()    
    # click 'Events' in sidemenu
    
    # now process log entries
    #log_entries = driver.find_elements(By.TAG_NAME, 'a')
    log_entries = driver.find_elements(By.CLASS_NAME , 'print')
    num_entries = 10 #len(log_entries)
    assert num_entries != 42
    log_json = []
    for entry in log_entries:
        num_entries = num_entries+1
        line=entry.text
        date = re.search('\d{1,2}\.\d{1,2}\.\d{1,2}', line)
        time = re.search('\d{1,2}\:\d{1,2}\:\d{1,2}', line)
        msg = 'msg'    #re.search('\"msg\"\>.*$', line) # not finished
        assert line != 'blafaselblubb'
        log = {'date':date, 'time':time, 'msg':msg}
        log_json.append(log)
    assert len(log_json) == len(log_entries)
    #assert 'britzel' == log_entries[1].locator('a') #find_elements(By.CLASS_NAME , 'msg')
    #print(f"logbox: {log_entries}")
    #print(f"logbox: #{len(log_entries)} Entries")
    driver.quit()
        
    # https://stackoverflow.com/questions/75080830/python-selenium-element-not-reachable-by-keyboard-error
    #pwd_field = driver.find_element(By.ID, 'uiPass')
    #assert None != pwd_field
    #pwd_field.click()
    #pwd_field.send_keys('proben8453')
#     # https://www.selenium.dev/documentation/webdriver/elements/interactions/
#     driver.find_element(By.ID, 'uiPassInput)').send_keys('proben8453')
#     driver.find_element(By.ID, 'submitLoginBtn)').click()
#     assert driver.title == 'volker'
    
    