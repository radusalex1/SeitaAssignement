import pytest
from rest_api import app

@pytest.fixture()
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_forecast_wrong_format_now_date(client):
    #arrange
    #act
    response = client.get("/forecasts",query_string={'now':'2020-11-0200:00:00Z','then':'2020-11-02T00:00:00Z'})

    #assert
    assert response.json == {'error': 'Parameter \'now\' is wrong formated.Please provide iso format'}

def test_get_forecast_wrong_format_then_date(client):
    #arrange
    #act
    response = client.get("/forecasts",query_string={'now':'2020-11-02T00:00:00Z','then':'2020-11-0200:00:00Z'})

    #assert
    assert response.json == {'error': 'Parameter \'then\' is wrong formated.Please provide iso format'}

def test_get_forecast_missing_parameter_now(client):
    #arrange
    #act
    response = client.get("/forecasts",query_string={'then':'2020-11-02T00:00:00Z'})

    #assert
    assert response.json == {'error': 'Missing \'now\' parameter'}

def test_get_forecast_missing_parameter_then(client):
    #arrange
    #act
    response = client.get("/forecasts",query_string={'now':'2020-11-02T00:00:00Z'})

    #assert
    assert response.json == {'error': 'Missing \'then\' parameter'}

def test_get_forecast(client):
    #arrange
    #act
    response = client.get("/forecasts",query_string={'now':'2020-11-02T00:00:00Z','then':'2020-11-02T00:00:00Z'})

    #assert
    assert response.json == {'data': []}

def test_get_tomorrow_wrong_format_now_date(client):
    #arrange
    #act
    response = client.get("/tomorrow",query_string={'now':'2020-11-0200:00:00Z'})

    #assert
    assert response.json == {'error': 'Parameter \'now\' is wrong formated.Please provide iso format'}

def test_get_tomorrow_missing_parameter(client):
    #arrange
    #act
    response = client.get("/tomorrow")

    #assert
    assert response.json == {'error': 'Missing \'now\' parameter'}

def test_get_tomorrow(client):
    #arrange
    #act
    response = client.get("/tomorrow",query_string={'now':'2020-11-02T00:00:00Z'})

    #assert
    assert response.json == {'data': {'sunny': False, 'warm': False, 'windy': True}}