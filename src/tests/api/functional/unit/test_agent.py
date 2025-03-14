import asyncio
import pytest
from unittest.mock import AsyncMock, patch
from src.loguru_logger import logger

@pytest.mark.parametrize("test_case", [
    {   # ✅ Low Risk - Should Approve
        "input": {"name": "Alice Johnson", "age": 40, "revenue": 120000, "credit_score": 780, "loan_amount": 25000},
        "expected": "Approved"
    },
    {   # ❌ High Risk - Should Reject
        "input": {"name": "Bob Smith", "age": 32, "revenue": 45000, "credit_score": 600, "loan_amount": 30000},
        "expected": "Rejected"
    }
])
def test_static_loan_decisions(agent, test_case):
    """
    Unit test for loan decision evaluation based on static test cases.
    """
    response, status = agent.evaluate_loan_application(**test_case["input"])
    assert response["loan_decision"] == test_case["expected"]

@pytest.mark.asyncio
async def test_dynamic_loan_decisions(agent, synthetic_data):
    """
    Asynchronous test for dynamically generated loan applications using a mocked AI response.
    """
    mock_decisions = ["Approved", "Rejected", "Conditional Approval"]

    with patch.object(agent, "evaluate_loan_application", new=AsyncMock()) as mock_agent:
        mock_agent.side_effect = [{"loan_decision": decision} for decision in mock_decisions]

        for idx, application in enumerate(synthetic_data[:3]):
            response = await agent.evaluate_loan_application(**application)
            assert response["loan_decision"] in mock_decisions, f"Unexpected decision: {response}"
            logger.info(f"✅ Loan application {idx + 1}: {response}")

@pytest.mark.parametrize("invalid_case", [
    {"name": "", "age": 25, "revenue": 60000, "credit_score": 700, "loan_amount": 20000},  # Empty name
    {"name": "John Doe", "age": 17, "revenue": 60000, "credit_score": 700, "loan_amount": 20000},  # Age below 18
    {"name": "John Doe", "age": 40, "revenue": -1000, "credit_score": 700, "loan_amount": 20000},  # Negative revenue
    {"name": "John Doe", "age": 40, "revenue": 60000, "credit_score": 290, "loan_amount": 20000},  # Invalid credit score
    {"name": "John Doe", "age": 40, "revenue": 60000, "credit_score": 700, "loan_amount": -5000}  # Negative loan amount
])
def test_invalid_input_cases(agent, invalid_case):
    """
    Tests that invalid input cases return an error response.
    """
    response, status = agent.evaluate_loan_application(**invalid_case)
    assert "errors" in response, "Validation errors were expected but not found."
    logger.warning(f"⚠️ Invalid input case caught: {response}")

@pytest.mark.asyncio
async def test_ai_generated_case(generator):
    """
    Generates an AI-based financial document, saves it to a file,
    reloads it, and performs comprehensive validation.
    """
    test_case = {"credit_score": 720, "revenue": 90000, "loan_amount": 35000}

    # Generate and save AI test case
    ai_response = await asyncio.to_thread(generator.generate_ai_test_case, **test_case)

    # Validate AI-generated response
    assert isinstance(ai_response, str), "AI-generated document should be a string."
    assert ai_response.strip(), "AI-generated document should not be empty."
    assert any(key in ai_response for key in ["Loan Amount", "Credit Score"]), "Generated document lacks financial details."

    # Load and validate saved AI test case
    loaded_data = generator.load_ai_test_case()
    assert isinstance(loaded_data, dict), "Loaded AI test data should be a dictionary."
    assert "generated_document" in loaded_data, "Saved data should contain 'generated_document' key."
    assert loaded_data["generated_document"].strip(), "Saved AI document should not be empty."
    assert loaded_data["input"] == test_case, "Test case input mismatch in saved data."

    logger.info("\n✅ AI-Generated Test Case Successfully Processed & Validated.")
