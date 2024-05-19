import pytest
import re
from playwright.sync_api import Page, expect
from playwright.sync_api import sync_playwright, Playwright

ID_FIELD_USER='uiViewUser'
ID_FIELD_PWD='uiPassInput'
ID_BTN_OK = 'submitLoginBtn'
ID_MENU_SYSTEM = '#sys'
ID_MENU_LOG = '#log'

FRITZ_BOX_URL='http://fritz.box'
FRITZ_BOX_TITLE='FRITZ!Box'
FRITZ_BOX_TITLE_AFTER_LOGIN='FRITZ!Box 6591 Cable'


def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch()
    page = browser.new_page()
    page.goto(FRITZ_BOX_URL)
    expect (page).to_have_title(FRITZ_BOX_TITLE)
    
    user_select = page.locator('#'+ID_FIELD_USER)
    user_select.select_option(value='supermann')
    
    password_field = page.locator('#'+ID_FIELD_PWD)
    password_field.type('proben8453')
    page.locator('#'+ID_BTN_OK).click()
    expect (page).to_have_title(FRITZ_BOX_TITLE_AFTER_LOGIN)
    
    page.locator(ID_MENU_SYSTEM).click()
    page.locator(ID_MENU_LOG).click()
    logbox = page.locator('#logBox')
    expect (logbox).to_have_class('scroll_area all-area')
    entries = logbox.get_by_role('link').all()
    expect (len(entries)) == 42
    browser.close()

def test_fritz():
    with sync_playwright() as playwright:
        run(playwright)