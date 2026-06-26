from http import HTTPStatus

from fastapi.testclient import TestClient

from recomendador.app import app


def test_read_root():
    client = TestClient(app)

    response = client.get('/')

    assert response.json() == {'message': 'Hello, World!'}
    assert response.status_code == HTTPStatus.OK
