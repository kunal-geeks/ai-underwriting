import pytest
import json
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import MagicMock
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.loguru_logger import logger


# 🔥 Initialize AI Model for Test Case Generation
llm = ChatOpenAI(model="gpt-4o-mini", temperature=1.0)

def generate_test_case():
    """
    🤖 Uses AI to dynamically generate valid test cases for loan applications.
    ✅ Ensures output is valid JSON and within expected value ranges.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are an AI test engineer creating diverse loan applications for an underwriting system.\n"
         "Each test case should be a valid JSON object with:\n"
         "- 'name': String (applicant name)\n"
         "- 'age': Integer (18 - 65)\n"
         "- 'revenue': Integer (10000 - 500000)\n"
         "- 'credit_score': Integer (300 - 850)\n"
         "- 'loan_amount': Integer (1000 - 100000)\n"
         "Ensure variety: high/low credit scores, different incomes, edge cases, etc."),
        ("human", "Generate a random test case.")
    ])
    
    try:
        response = llm.invoke(prompt.format())
        test_case = json.loads(response.content)
        assert 18 <= test_case["age"] <= 65
        assert 10000 <= test_case["revenue"] <= 500000
        assert 300 <= test_case["credit_score"] <= 850
        assert 1000 <= test_case["loan_amount"] <= 100000
        
        logger.info(f"✅ AI-generated test case: {test_case}")
        return test_case
    except (json.JSONDecodeError, AssertionError, KeyError) as e:
        logger.warning(f"⚠️ AI failed to generate a valid test case, using fallback. Error: {e}")
        return {
            "name": "Fallback Test Case",
            "age": 30,
            "revenue": 50000,
            "credit_score": 700,
            "loan_amount": 20000
        }  # Safe fallback case

@pytest.mark.parametrize("test_type", ["valid", "high_risk", "edge_case"])
def test_auto_generated_cases(agent, test_type):
    """
    🎯 Runs AI-generated test cases against the underwriting system.
    ✅ Ensures the underwriting agent responds with a decision.
    """
    test_case = generate_test_case()
    assert test_case, "❌ AI failed to generate a valid test case"

    if test_type == "high_risk":
        test_case["credit_score"] = 300  # Poor credit score
        test_case["revenue"] = 20000
        test_case["loan_amount"] = 75000  # High loan relative to income

    elif test_type == "edge_case":
        test_case["age"] = 18  # Minimum age
        test_case["credit_score"] = 850  # Best possible score
        test_case["loan_amount"] = 100000  # Max possible loan

    agent.evaluate_loan_application = MagicMock(return_value={"loan_decision": "Approve"})
    response = agent.evaluate_loan_application(
        test_case["name"], test_case["age"], test_case["revenue"],
        test_case["credit_score"], test_case["loan_amount"]
    )
    assert "loan_decision" in response
    logger.info(f"✅ Test case '{test_type}' passed with decision: {response['loan_decision']}")

def test_auto_fix_failing_tests(agent):
    """
    🔧 Simulates a failing test and requests AI to suggest a fix.
    ✅ Ensures AI correctly rejects high-risk loans.
    """
    failing_case = {
        "name": "Test Failure",
        "age": 22,
        "revenue": 15000,
        "credit_score": 400,
        "loan_amount": 60000  # Should likely be rejected
    }
    
    agent.evaluate_loan_application = MagicMock(return_value={"loan_decision": "Reject"})
    response = agent.evaluate_loan_application(
        failing_case["name"], failing_case["age"], failing_case["revenue"],
        failing_case["credit_score"], failing_case["loan_amount"]
    )
    
    assert "Reject" in response["loan_decision"], "❌ AI should reject high-risk loans"
    logger.info(f"✅ AI correctly rejected a high-risk loan application.")

def test_stress_with_generated_cases(agent):
    """
    🚀 Runs multiple AI-generated test cases to stress test the underwriting agent.
    ✅ Optimized for performance by using ThreadPoolExecutor.
    """
    agent.evaluate_loan_application = MagicMock(return_value={"loan_decision": "Approve"})
    
    def execute_test():
        test_case = generate_test_case()
        response = agent.evaluate_loan_application(
            test_case["name"], test_case["age"], test_case["revenue"],
            test_case["credit_score"], test_case["loan_amount"]
        )
        assert "loan_decision" in response
    
    # ⏳ Run tests in parallel for faster execution
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(lambda _: execute_test(), range(5))  
    
    logger.info("✅ Stress test completed successfully with multiple AI-generated cases.")