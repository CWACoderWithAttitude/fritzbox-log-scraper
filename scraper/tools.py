"""Tools & helpers to assist using selenium"""

from selenium import webdriver
from datetime import datetime


def build_ff_options():
    ff_options = webdriver.FirefoxOptions()
    ff_options.add_argument("-headless")
    return ff_options


sel_url = "http://selenium-hub:4444/wd/hub"


def get_remote_ff():
    driver = webdriver.Remote(
        command_executor=sel_url,
        options=build_ff_options(),  # {'browserName': 'firefox', 'javascriptEnabled': True}
    )
    return driver


def get_remote_chrome():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.setCapability("browserVersion", "100")
    # chrome_options.setCapability("platformName", "Windows")
    # // Showing a test name instead of the session id in the Grid UI
    # chrome_options.setCapability("se:name", "My simple test")
    # // Other type of metadata can be seen in the Grid UI by clicking on the
    # // session info or via GraphQL
    # chrome_options.setCapability("se:sampleMetadata", "Sample metadata value")
    # driver = new RemoteWebDriver(new URL("http://gridUrl:4444"), chromeOptions);
    driver = webdriver.Remote(command_executor=sel_url, options=chrome_options)
    return driver


def get_timestamp():
    now = datetime.now()  # current date and time
    # date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    date_time = now.strftime("%Y-%m-%d_%H_%M_%S")
    print("date and time:", date_time)
    return date_time
