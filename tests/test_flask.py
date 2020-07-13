import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    test_client = app.test_client()
    yield test_client
    test_client.delete()


def test_flask_testpage(client):
    result = client.get('/test')
    assert b'test' == result.data