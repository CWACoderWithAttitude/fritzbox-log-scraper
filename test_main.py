from main import app
from fastapi.testclient import TestClient
from ff_scraper import get_logs
from pytest_mock import mocker
from scraper.logscraper import get_logs_from_fritzbox

test_client = TestClient(app)


def test_read_default():
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Ei Gude!"}


# https://pytest-with-eric.com/mocking/pytest-mocking/#Mock-External-Rest-API-Calls
def Xtest_read_mocked_logs(mocker):
    mock_logs = {"msg": "Hallo Bad Vilbel"}
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = mock_logs

    response = test_client.get("/logs")

    assert response.status_code == 200
    # assert response.json() == {"logs": logs}


# def test_get_logs_contains_log_key():
#    response = test_client.get("/logs")
#    rj = response.json()
#    assert "logs" in rj.keys()


def test_get_logs_contains_log_key_mocked(mocker):
    mock_data = [
        {
            "date": "11.06.24",
            "time": "10:58:51",
            "msg": ":51\nAnmeldung des Benutzers supermann an der FRITZ!Box-Benutzeroberfläche von IP-Adresse 192.168.178.24. [2 Meldungen seit 11.06.24 10:58:30]",
        },
        {
            "date": "11.06.24",
            "time": "09:59:11",
            "msg": ":11\nWLAN-Gerät hat sich neu angemeldet (2,4 GHz), 72 Mbit/s, PC-04-34-F6-10-38-B1, IP 192.168.178.131, MAC 04:34:F6:10:38:B1.",
        },
    ]

    # Create a mock response object with a .json() method that returns the mock data
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = mock_data

    # Patch 'requests.get' to return the mock response
    # mocker.patch("scraper.logscraper.get_logs_from_fritzbox", return_value=mock_response)
    mocker.patch.object(logscraper, "get_logs_from_fritzbox", return_value=mock_response)

    # Call the function
    result = get_logs_from_fritzbox()

    # Assertions to check if the returned data is as expected
    assert type(result) == "bubu"
    assert result == mock_data
    # assert type(result) is dict
    # assert result["temperature"] == "+7 °C"
