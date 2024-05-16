from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# enable headless mode in Selenium
# options = Options()
# options.add_argument('--headless=new')chrome_options = webdriver.ChromeOptions()
sel_url = 'http://host.docker.internal:3001'

def build_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    return chrome_options

def get_driver():
    chrome_options = build_chrome_options()
    driver = webdriver.Remote(
        command_executor=sel_url,
        options=chrome_options
    )
    return driver

def get_ff():
  # Define the desired capabilities for Firefox
    desired_capabilities = DesiredCapabilities.FIREFOX.copy()

    # Initialize the remote WebDriver pointing to the Selenium Grid server
    # Replace "GRID_HOST" and "GRID_PORT" with the actual host and port of your Selenium Grid server
    driver = webdriver.Remote(
        command_executor='http://host.docker.internal:3002', #/playwright/firefox',
        options=webdriver.FirefoxOptions()
    )
    return driver
#get_driver().driver.get('http://fritz.box')
#print(f"Title: {driver.title()}")
# scraping logic...

# release the resources allocated by Selenium and shut down the browser
#driver.quit()
