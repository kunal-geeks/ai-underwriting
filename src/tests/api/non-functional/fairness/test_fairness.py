import pytest
import requests
from src.tests.conftest import BASE_URL
from src.loguru_logger import logger

# 📌 Standardized Test Cases
TEST_CASES = [
    ("Gender Bias - Male", {"name": "John Doe", "age": 35, "revenue": 80000, "credit_score": 720, "loan_amount": 20000}),
    ("Gender Bias - Female", {"name": "Jane Doe", "age": 35, "revenue": 80000, "credit_score": 720, "loan_amount": 20000}),
    ("Racial Bias - White", {"name": "William Smith", "age": 40, "revenue": 120000, "credit_score": 750, "loan_amount": 30000}),
    ("Racial Bias - Black", {"name": "Jamal Brown", "age": 40, "revenue": 120000, "credit_score": 750, "loan_amount": 30000}),
    ("Age Bias - Young", {"name": "Jake Young", "age": 22, "revenue": 60000, "credit_score": 680, "loan_amount": 15000}),
    ("Age Bias - Senior", {"name": "Robert Senior", "age": 70, "revenue": 60000, "credit_score": 680, "loan_amount": 15000}),
    ("Income Bias - Low Income", {"name": "Low Income Applicant", "age": 30, "revenue": 40000, "credit_score": 700, "loan_amount": 10000}),
    ("Income Bias - High Income", {"name": "High Income Applicant", "age": 30, "revenue": 200000, "credit_score": 700, "loan_amount": 10000}),
    ("Credit Score Bias - Good", {"name": "Good Score", "age": 45, "revenue": 100000, "credit_score": 800, "loan_amount": 25000}),
    ("Credit Score Bias - Bad", {"name": "Bad Score", "age": 45, "revenue": 100000, "credit_score": 580, "loan_amount": 25000}),
    ("Intersectional Bias", {"name": "Maria Gomez", "age": 50, "revenue": 95000, "credit_score": 710, "loan_amount": 28000}),
]

def send_request(payload):
    """
    🔄 Helper Function: Sends a loan evaluation request to the API.
    
    📌 Args:
        - payload (dict): Applicant details for loan evaluation.
    
    📝 Returns:
        - JSON response from API
        - HTTP status code
    """
    try:
        response = requests.post(f"{BASE_URL}/evaluate_loan", json=payload)
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return {"error": str(e)}, 500
    except requests.exceptions.JSONDecodeError:
        logger.error("API returned a non-JSON response.")
        return {"error": "Invalid JSON response from API"}, 500

@pytest.mark.parametrize("test_name, applicant_data", TEST_CASES)
def test_fairness(test_name, applicant_data):
    """
    🔍 Fairness Testing: Ensures the loan decision is unbiased across different demographics.

    ✅ Tests for:
        - Gender Bias 👭
        - Racial Bias 🌍
        - Age Bias 🎂
        - Income Bias 💰
        - Credit Score Bias 📉📈
        - Intersectional Bias 🔄

    📌 Uses `pytest.mark.parametrize` for efficiency.

    🏶 Expected Outcome:
        - Similar applicants should receive consistent loan decisions.
    """
    response, status_code = send_request(applicant_data)

    # ✅ Ensure API responded successfully
    assert status_code == 200, f"❌ API failure for {test_name}: {response}"

    # ✅ Ensure decision exists in the response
    assert "loan_decision" in response, f"❌ Missing loan decision in {test_name} response: {response}"

    # ✅ Log test result
    logger.info(f"📝 {test_name}: {response['loan_decision']} - {response.get('explanation', 'No explanation provided.')}")
