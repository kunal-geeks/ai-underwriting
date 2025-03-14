import pytest
import requests
import asyncio
from src.ai_agent.utils import StatusCode
from src.tests.conftest import BASE_URL
from unittest.mock import patch

def test_api_health_check():
    """Ensure API is up and running."""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json().get("status") == "healthy"


def test_missing_fields():
    """Test API behavior when required fields are missing."""
    response = requests.post(f"{BASE_URL}/evaluate_loan", json={"name": "John Doe", "age": 35})
    assert response.status_code == 400
    assert "errors" in response.json()


def test_invalid_json_format():
    """Test API behavior when receiving malformed JSON."""
    response = requests.post(f"{BASE_URL}/evaluate_loan", data="Invalid JSON")
    assert response.status_code == 400


def test_large_payload():
    """Test how the API handles a very large request payload."""
    large_application = {
        "name": "John Doe",
        "age": 35,
        "revenue": 1000000,
        "credit_score": 750,
        "loan_amount": 50000,
        "extra_field_1": "test" * 1000,
        "extra_field_2": "test" * 1000,
    }
    response = requests.post(f"{BASE_URL}/evaluate_loan", json=large_application)
    assert response.status_code == 400  # Should reject unexpected fields


@pytest.mark.asyncio
async def test_high_concurrency(mock_underwriting_agent):
    """Simulate multiple concurrent API requests with mocked responses."""
    applications = [
        {"name": f"User {i}", "age": 30, "revenue": 80000, "credit_score": 720, "loan_amount": 15000}
        for i in range(20)
    ]

    async def make_request(app_data):
        return requests.post(f"{BASE_URL}/evaluate_loan", json=app_data)

    tasks = [make_request(app) for app in applications]
    responses = await asyncio.gather(*tasks)

    for response in responses:
        assert response.status_code == 200
        assert "loan_decision" in response.json()


def test_slow_response_handling(mock_underwriting_agent):
    """Test API behavior when the AI model takes too long to respond."""

    async def slow_response(*args, **kwargs):
        await asyncio.sleep(5)  # Simulate delay
        return {"loan_decision": "Approved"}, StatusCode.SUCCESS

    mock_underwriting_agent.side_effect = slow_response  # Override the fixture's default behavior

    response = requests.post(f"{BASE_URL}/evaluate_loan", json={
        "name": "Delayed User",
        "age": 45,
        "revenue": 100000,
        "credit_score": 700,
        "loan_amount": 30000
    })
    assert response.status_code == 200
    assert "loan_decision" in response.json()

def test_internal_server_error_handling():
    """Test how the API handles unexpected internal errors."""

    response = requests.post(f"{BASE_URL}/evaluate_loan", json={
        "name": "Error Test",  # ✅ This will now trigger an exception
        "age": 40,
        "revenue": 90000,
        "credit_score": 710,
        "loan_amount": 25000
    })

    print(f"🔹 Response: {response.status_code}, {response.text}")  # Debugging

    assert response.status_code == 500, f"Expected 500, but got {response.status_code} with body {response.text}"





