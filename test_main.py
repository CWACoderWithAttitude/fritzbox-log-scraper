from main import app
from fastapi.testclient import TestClient
from ff_scraper import get_logs
from pytest_mock import mocker

client = TestClient(app)

#logs = get_logs()

def test_read_default():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

def Xtest_read_logs():
    response = client.get("/logs")
    assert response.status_code == 200
    assert response.json() == {"logs": logs}
    
def test_read_logs(mocker):
    response = client.get("/logs")
    client.get("/logs")
    assert response.status_code == 200
# https://pytest-with-eric.com/mocking/pytest-mocking/#Mock-External-Rest-API-Calls
def test_read_mocked_logs(mocker):
    mock_logs = {"msg": "Hallo Bad Vilbel"}
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = mock_logs
    
    
    
    response = client.get("/logs")

    assert response.status_code == 200
    #assert response.json() == {"logs": logs}
