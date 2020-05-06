import pytest

from sample_app.app import app


@pytest.fixture
def client():
    yield app.test_client()
