import pytest
import requests
from src.tests.conftest import BASE_URL

def assert_error_response(response, expected_status_code, expected_errors):
    """Helper function to assert error responses."""
    assert response.status_code == expected_status_code, f"Expected {expected_status_code}, got {response.status_code}"
    data = response.json()  
    assert "errors" in data, "Expected 'errors' field in response"
    for error in expected_errors:
        assert any(error in e for e in data["errors"]), f"Expected error message: {error}"

def test_evaluate_loan_approval(valid_application):
    """Test loan approval decision for a valid applicant."""
    response = requests.post(f"{BASE_URL}/evaluate_loan", json=valid_application)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response: {response.text}"
    
    data = response.json()
    assert "loan_decision" in data, "Missing 'loan_decision' in response"
    assert data["loan_decision"] == "Approved", f"Unexpected loan decision: {data['loan_decision']}"

def test_high_risk_rejection(high_risk_application):
    """Test that high-risk applicants are rejected."""
    response = requests.post(f"{BASE_URL}/evaluate_loan", json=high_risk_application)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response: {response.text}"
    
    data = response.json()
    assert "loan_decision" in data, "Missing 'loan_decision' in response"
    assert data["loan_decision"] == "Rejected", f"Unexpected loan decision: {data['loan_decision']}"

@pytest.mark.parametrize("incomplete_data,expected_errors", [
    ({"name": "John Doe", "age": 35}, ["Missing revenue", "Missing credit_score", "Missing loan_amount"]),
    ({"name": "Emma Watson", "revenue": 75000}, ["Missing age", "Missing credit_score", "Missing loan_amount"]),
    ({}, ["Missing name", "Missing age", "Missing revenue", "Missing credit_score", "Missing loan_amount"])
])
def test_missing_fields(incomplete_data, expected_errors):
    """Test API response when required fields are missing."""
    response = requests.post(f"{BASE_URL}/evaluate_loan", json=incomplete_data)
    assert_error_response(response, 400, expected_errors)

@pytest.mark.parametrize("boundary_case,expected_status_code,expected_errors", [
    ({"name": "Tom Hardy", "age": 18, "revenue": 25000, "credit_score": 850, "loan_amount": 5000}, 200, []),
    ({"name": "Samantha Green", "age": 100, "revenue": 180000, "credit_score": 720, "loan_amount": 50000}, 200, []),
    ({"name": "Daniel Craig", "age": 40, "revenue": 500000, "credit_score": 300, "loan_amount": 5000}, 200, []),
    ({"name": "Robert Downey", "age": 35, "revenue": 60000, "credit_score": 900, "loan_amount": 10000}, 400, ["Invalid credit score"])
])
def test_boundary_values(boundary_case, expected_status_code, expected_errors):
    """Test edge cases for credit score, loan amount, and age."""
    response = requests.post(f"{BASE_URL}/evaluate_loan", json=boundary_case)
    if expected_errors:
        assert_error_response(response, expected_status_code, expected_errors)
    else:
        assert response.status_code == expected_status_code

def test_large_loan_amount():
    """Test how the system handles an extremely high loan amount."""
    application = {
        "name": "Elon Musk",
        "age": 45,
        "revenue": 10000000,
        "credit_score": 800,
        "loan_amount": 100000000  # Very large loan amount
    }
    response = requests.post(f"{BASE_URL}/evaluate_loan", json=application)
    assert_error_response(response, 400, ["Loan exceeds business max limit"])

def test_negative_values():
    """Test API behavior when negative values are provided."""
    negative_application = {
        "name": "Negative Test",
        "age": -25,
        "revenue": -50000,
        "credit_score": -300,
        "loan_amount": -20000
    }
    response = requests.post(f"{BASE_URL}/evaluate_loan", json=negative_application)
    assert_error_response(response, 400, ["Invalid age", "Invalid revenue", "Invalid credit score", "Invalid loan amount"])
    
def test_non_numeric_values():
    """Test API response when non-numeric values are passed for numeric fields."""
    invalid_application = {
        "name": "String Test",
        "age": "forty",
        "revenue": "one hundred thousand",
        "credit_score": "seven hundred",
        "loan_amount": "fifty thousand"
    }
    response = requests.post(f"{BASE_URL}/evaluate_loan", json=invalid_application)
    assert_error_response(response, 400, [
        "❌ Invalid age: must be an integer between 18 and 100.",
        "❌ Invalid revenue: must be a positive number.",
        "❌ Invalid credit score: must be an integer between 300 and 850.",
        "❌ Invalid loan amount: must be a positive number."
    ])

def test_api_unavailable():
    """Test API error handling when the service is down."""
    invalid_url = "http://127.0.0.1:1234/evaluate_loan"  # Incorrect port
    with pytest.raises(requests.exceptions.ConnectionError):
        requests.post(invalid_url, json={})
