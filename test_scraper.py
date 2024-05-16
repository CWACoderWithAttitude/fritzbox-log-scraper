import pytest
from fritz_scraper import get_ff, get_driver
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options

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


def get_remote_ff():
    ff_options = webdriver.FirefoxOptions()
    ff_options.add_argument("-headless")
    driver = webdriver.Remote(
        command_executor=sel_url,
        options=ff_options  #{'browserName': 'firefox', 'javascriptEnabled': True}
    )
    return driver
def test_get_ff():
    driver = get_remote_ff()

    assert driver != 'bubu'
    driver.quit()
    
def test_get_heise():
    driver = get_remote_ff()
    driver.get('https://www.heise.de')
    assert 'heise online - IT-News, Nachrichten und Hintergründe | heise online' == driver.title
    driver.quit()