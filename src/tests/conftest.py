import json
import pytest
from unittest.mock import AsyncMock, patch
from src.ai_agent.model import UnderwritingAgent
from src.tests.synthetic_data import SyntheticDataGenerator

#BASE_URL = "http://127.0.0.1:5001"
BASE_URL = "http://underwriting_app_local:5001"


@pytest.fixture(scope="module")
def agent():
    """
    Initializes the AI underwriting agent.
    """
    return UnderwritingAgent()

@pytest.fixture(scope="module")
def synthetic_data():
    """
    Generates synthetic test cases for dynamic testing.
    """
    generator = SyntheticDataGenerator()
    test_cases = generator.generate_bulk_applications(n=20)
    
    # Save test cases for debugging consistency
    with open("synthetic_test_cases.json", "w") as f:
        json.dump(test_cases, f, indent=4)

    return test_cases

@pytest.fixture(scope="module")
def generator():
    """
    Generates the instance of SyntheticDataGenerator.
    """
    return SyntheticDataGenerator()

@pytest.fixture
def valid_application():
    """Returns a valid loan application with typical values."""
    return {
        "name": "Alice Johnson",
        "age": 40,
        "revenue": 120000,
        "credit_score": 780,
        "loan_amount": 25000
    }

@pytest.fixture
def high_risk_application():
    """Returns an application that should be rejected due to high risk."""
    return {
        "name": "Bob Smith",
        "age": 50,
        "revenue": 40000,
        "credit_score": 600,
        "loan_amount": 30000
    }

@pytest.fixture
def sample_payload():
    """
    📝 Fixture: Provides a standard loan application payload.
    Ensures consistency across tests.
    """
    return {
        "name": "Test User",
        "age": 35,
        "revenue": 90000,
        "credit_score": 720,
        "loan_amount": 20000
    }
    
@pytest.fixture
def mock_underwriting_agent(agent):
    """
    Mock the UnderwritingAgent methods to avoid real API calls and speed up tests.
    """
    with patch.object(agent, "evaluate_loan_application", new_callable=AsyncMock) as mock_method:
        mock_method.return_value = {
            "applicant": "Test User",
            "loan_decision": "Approved",
            "explanation": "Mocked response for fast testing."
        }
        yield mock_method


@pytest.fixture
def mock_openai_api():
    """
    Mock OpenAI API responses to avoid real API calls.
    """
    with patch("src.ai_agent.model.ChatOpenAI.invoke", new_callable=AsyncMock) as mock_chat_openai:
        mock_chat_openai.return_value.content = "Mocked AI Response"
        yield mock_chat_openai


@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(node, call, report):
    """Capture screenshot on test failure (for Selenium tests)."""
    if report.failed and "driver" in node.funcargs:
        driver = node.funcargs["driver"]
        try:
            driver.save_screenshot(f"reports/{node.name}.png")
        except Exception:
            pass  # Avoid crashing tests if screenshot fails



