import pytest, re

DATA="""
<div class="scroll_area all-area" id="logBox">
    <a class="print" target="_blank" href="/help/help.lua?sid=239811f51679f5ea&amp;helppage=hilfe_syslog_504.html">
        <div class="date">17.05.24</div>
        <div class="time">23:55:21</div>
        <div class="msg">Anmeldung des Benutzers supermann an der FRITZ!Box-Benutzeroberfläche von IP-Adresse
            192.168.178.24.</div>
    </a>"""

REGEXP_DATE = r'\d{1,2}\.\d{1,2}\.\d{1,2}'
REGEXP_TIME = r'\d{1,2}\:.\d{1,2}\:\d{1,2}'
EXPECTED_MSG='Anmeldung des Benutzers supermann an der FRITZ!Box-Benutzeroberfläche von IP-Adresse 192.168.178.24.'

def test_match_date():
    date_match = re.findall(REGEXP_DATE, DATA)
    assert len(date_match) == 1
    
def test_get_date_match():
    date_match = re.search(REGEXP_DATE, DATA)
    assert date_match.group() == '17.05.24'
    
def test_match_time():
    time_match = re.findall(REGEXP_TIME, DATA)
    assert len(time_match) == 1

def test_get_time_match():
    time_match = re.search(REGEXP_TIME, DATA)
    assert time_match.group() == '23:55:21'

def test_match_msg():
    msg_match = re.findall(REGEXP_MSG, DATA)
    assert len(msg_match) == 1
    
#REGEXP_MSG = r'\<div class=\"msg\"\>.*\<\/dev\>'
REGEXP_MSG = r'\<div class=\"msg\"\>.*'

def test_get_msg_match():
    msg_match = re.findall(REGEXP_MSG, DATA)
    assert msg_match[0] == EXPECTED_MSG