import pytest, re, os
#from fritz_scraper import get_ff, get_driver
from ff_scraper import get_remote_ff
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
FRITZ_BOX_TITLE_AFTER_LOGIN='FRITZ!Box 6591 Cable'
    
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
    driver = None
    try:
        driver = get_remote_ff()
        driver.get(os.environ['FRITZBOX_URL'])
        # https://stackoverflow.com/questions/7867537/how-to-select-a-drop-down-menu-value-with-selenium-using-python
        select = Select(driver.find_element(By.ID, 'uiViewUser'))
        select.select_by_value('supermann')
        
        #select.select_by_value(os.environ['FRITZBOX_USER'])
        # https://www.browserstack.com/guide/understanding-selenium-timeouts
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, ID_PWD_FIELD)))
        pwd_field = driver.find_element(By.ID, ID_PWD_FIELD)
        assert None != pwd_field
        pwd_field.click()
        pwd_field.send_keys(os.environ['FRITZBOX_PASSWORD'])
        #select.select_by_value(os.environ['FRITZBOX_USER'])
    except:
        print("get_logs > Error1")
        if driver is not None:
            driver.quit()
    try:
        #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, ID_PWD_FIELD)))
        driver.find_element(By.ID, ID_BTN_OK).click()
        return driver
        #assert driver.title == FRITZ_BOX_TITLE_AFTER_LOGIN
    except:
        print("get_logs > Error2")
        if driver is not None:
            driver.quit()

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
       
def _test_get_remote_ff():
    try:
        driver = get_remote_ff()
        assert driver != 'bubu'
    except:
        if driver is not None:
            driver.quit()

def _test_get_page():
    try:
        driver = get_remote_ff()
        driver.get(url='https://www.heise.de')
        assert driver.title == 'heise online - IT-News, Nachrichten und Hintergründe | heise online'
    except:
        if driver is not None:
            driver.quit()
     
def test_login_to_fritzbox():    
    driver = fritz_login(None, None, None)
    assert driver.title == FRITZ_BOX_TITLE_AFTER_LOGIN
    logbox = get_logbox(driver=driver)
    assert logbox != "bubu"
    log_json = get_log_entries_from_logbox(logbox)
    assert len(log_json) != 42
    
def get_logbox(driver : webdriver):
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'sys')))
        sys = driver.find_element(By.ID, 'sys')
        sys.click()
        #print(f"log: {sys}")
    except:
        print("get_logs > Error at click sys-menu item")
        if driver is not None:
            driver.quit()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'log')))
        log = driver.find_element(By.ID, 'log')
        log.click()
        #print(f"log: {log}")
    except:
        print("get_logs > Error4")
        if driver is not None:
            driver.quit()
    logbox = None
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'logBox')))
        logbox = driver.find_element(By.ID, 'logBox')
        #print(f"logbox: {logbox}")
    except:
        print("get_logs > Error5")
        if driver is not None:
            driver.quit()
    return logbox

def get_log_entries_from_logbox(driver : webdriver) -> list:
    log_entries = driver.find_elements(By.CLASS_NAME , 'print')
    num_entries = 10 #len(log_entries)
    assert num_entries != 0
    log_json = []
    try :
        for entry in log_entries:
            if len(log_json) > 10:
                log_json[:-1]
            else:
                print(f"test_select_logn_user: {len(log_json)}")
            num_entries = num_entries+1
            line=entry.text
            dateMatch = re.search(r'\d{1,2}\.\d{1,2}\.\d{1,2}', line)
            date = dateMatch.group() #line[dateMatch.start:dateMatch.end]
            time = re.search(r'\d{1,2}\:\d{1,2}\:\d{1,2}', line).group()
            msg = 'msg'    #re.search('\"msg\"\>.*$', line) # not finished
            REGEXP_MSG = r':\d{2}\n\S.*$'
            msg = re.search(REGEXP_MSG, line).group()
            log = {'date':date, 'time':time, 'msg':msg}
            print(log)
            log_json.append(log)
            print(f"len(log_json): {len(log_json)}")
    except:
        print(f"error ocurred while processing logs - returning {len(log_json)} from {len(log_entries)} logged messages...")
    #driver.quit()
    return log_json
        
    
    