"""
Test module for the hivebox application.
"""

import re
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from unittest.mock import patch

import pytest
from asyncmock import AsyncMock
from fastapi.testclient import TestClient

from ..main import app


@pytest.fixture
def client():
    """
    Set up the test client for FastAPI.
    """
    with TestClient(app) as client:
        yield client


def test_root_endpoint(client):
    """
    Test the / endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_version_endpoint(client):
    """
    Test the /version endpoint.
    """
    response = client.get("/version")
    assert response.status_code == 200
    # pylint: disable=line-too-long
    regex_pattern = "^(?P<major>0|[1-9]\\d*)\\.(?P<minor>0|[1-9]\\d*)\\.(?P<patch>0|[1-9]\\d*)(?:-(?P<prerelease>(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$"
    assert re.match(regex_pattern, response.json()["version"]) is not None


@pytest.mark.asyncio
async def test_temperature_endpoint_too_cold(client):
    mock_data = [
        {
            "sensors": [
                {
                    "unit": "°C",
                    "lastMeasurement": {
                        "createdAt": (
                            datetime.now(timezone.utc) - timedelta(minutes=30)
                        ).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "value": "9.9",
                    },
                },
            ],
        },
    ]
    with patch(
        "app.routers.temperature.fetch_sensebox_data",
        new_callable=AsyncMock,
        return_value=mock_data,
    ):
        response = client.get("/temperature")

        assert response.status_code == 200
        assert "average_temperature" in response.json()
        assert response.json()["average_temperature"] == 9.9
        assert response.json()["status"] == "Too Cold"


@pytest.mark.asyncio
async def test_temperature_endpoint_good(client):
    mock_data = [
        {
            "sensors": [
                {
                    "unit": "°C",
                    "lastMeasurement": {
                        "createdAt": (
                            datetime.now(timezone.utc) - timedelta(minutes=45)
                        ).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "value": "25",
                    },
                },
            ],
        },
    ]
    with patch(
        "app.routers.temperature.fetch_sensebox_data",
        new_callable=AsyncMock,
        return_value=mock_data,
    ):
        response = client.get("/temperature")

        assert response.status_code == 200
        assert "average_temperature" in response.json()
        assert response.json()["average_temperature"] == 25
        assert response.json()["status"] == "Good"


@pytest.mark.asyncio
async def test_temperature_endpoint_too_hot(client):
    mock_data = [
        {
            "sensors": [
                {
                    "unit": "°C",
                    "lastMeasurement": {
                        "createdAt": (
                            datetime.now(timezone.utc) - timedelta(minutes=15)
                        ).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "value": "36.1",
                    },
                },
            ],
        },
    ]
    with patch(
        "app.routers.temperature.fetch_sensebox_data",
        new_callable=AsyncMock,
        return_value=mock_data,
    ):
        response = client.get("/temperature")

        assert response.status_code == 200
        assert "average_temperature" in response.json()
        assert response.json()["average_temperature"] == 36.1
        assert response.json()["status"] == "Too Hot"
