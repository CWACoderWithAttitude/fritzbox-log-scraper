chrome_scraper.pyimport pytest, re, os
from fritz_scraper import get_ff, get_driver
from ff_scraper import
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
    
def build_ff_options():
    ff_options = webdriver.FirefoxOptions()
    ff_options.add_argument("-headless")
    return ff_options

def build_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    return options
    
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
       
def Xtest_get_remote_ff():
     driver = get_remote_ff()
     assert driver != 'bubu'

def get_remote_chrome():
    driver = webdriver.Remote(
        command_executor='http://192.168.178.153:4444/wd/hub',
        options=build_chrome_options()  #{'browserName': 'firefox', 'javascriptEnabled': True}
    )
    return driver
def Xtest_get_remote_chrome():
    """https://twomas.medium.com/selenium-grid-on-docker-in-a-raspberry-pi-for-automated-testing-on-chrome-caf59b5fb5c0
    """
    d = get_remote_chrome()
    d.get(url='https://www.heise.de')
    assert d.title == 'bubu'
    
def Xtest_get_page():
     driver = get_remote_ff()
     driver.get(url='https://www.heise.de')
     assert driver.title == 'heise online - IT-News, Nachrichten und Hintergründe | heise online'
     
def get_logs():
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
        assert driver.title == FRITZ_BOX_TITLE_AFTER_LOGIN
    except:
        print("get_logs > Error2")
        if driver is not None:
            driver.quit()
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


def Xtest_select_logon_user():
    driver = get_logs()    
    # click 'Events' in sidemenu
    
    # now process log entries
    #log_entries = driver.find_elements(By.TAG_NAME, 'a')
    log_entries = driver.find_elements(By.CLASS_NAME , 'print')
    num_entries = 10 #len(log_entries)
    assert num_entries != 0
    log_json = []
    for entry in log_entries:
        if len(log_json) > 10:
            exit
        else:
            print(f"test_select_logn_user: {len(log_json)}")
        num_entries = num_entries+1
        line=entry.text
        dateMatch = re.search(r'\d{1,2}\.\d{1,2}\.\d{1,2}', line)
        date = line[dateMatch.start:dateMatch.end]
        time = re.search(r'\d{1,2}\:\d{1,2}\:\d{1,2}', line)
        msg = 'msg'    #re.search('\"msg\"\>.*$', line) # not finished
        assert line != 'blafaselblubb'
        log = {'date':date, 'time':time, 'msg':msg}
        print(log)
        log_json.append(log)
    assert len(log_json)+1 == len(log_entries)
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
    
    