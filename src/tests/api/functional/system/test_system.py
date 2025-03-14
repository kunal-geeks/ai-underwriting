import psutil  
import pytest
import subprocess
import time
import requests
import os
from src.tests.conftest import BASE_URL
from src.loguru_logger import logger

# ================================
# 🔍 PROCESS MANAGEMENT HELPERS
# ================================
def find_process_on_port(port):
    """
    🧐 Identifies any process currently using the given port.
    """
    pids = []
    try:
        for conn in psutil.net_connections(kind="inet"):
            if conn.laddr.port == port and conn.pid:
                pids.append(conn.pid)
    except psutil.AccessDenied:
        logger.warning("Access denied while checking network connections.")
    return list(set(pids))  # Remove duplicate PIDs

def kill_process_on_port(port):
    """
    🛑 Terminates any process using the specified port to avoid conflicts.
    """
    pids = find_process_on_port(port)
    for pid in pids:
        try:
            proc = psutil.Process(pid)
            proc.terminate()  # Graceful shutdown 📴
            proc.wait(timeout=5)
            logger.info(f"Successfully terminated process {pid} on port {port}")
        except psutil.NoSuchProcess:
            logger.warning(f"Process {pid} not found.")
        except psutil.TimeoutExpired:
            logger.warning(f"Process {pid} did not terminate in time, forcing kill.")
            os.kill(pid, 9)  # Hard kill as last resort ⚡
        except psutil.AccessDenied:
            logger.error(f"Permission denied when trying to terminate process {pid}.")
            
            
# ================================
# 🛠️ FIXTURES: API SERVER MANAGEMENT
# ================================
@pytest.fixture(scope="module")
def start_api():
    """
    🚀 Starts the API server as a subprocess before running tests.
    Ensures a clean startup and graceful shutdown of the test environment.
    """
    logger.info("Starting API server...")
    process = subprocess.Popen(["python", "src/api/app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)  # ⏳ Allow time for the API to start
    yield process  # Provide the process to the test suite
    logger.info("Shutting down API server...")
    process.terminate()  # Cleanup: stop the API server
    process.wait()

# ================================
# ✅ HEALTH CHECK TEST
# ================================
def test_api_health(start_api):
    """
    🔍 Checks if the API is running and responding properly.
    """
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200, "API health check failed!"
    assert response.json().get("status") == "healthy", "Unexpected health check response!"

# ================================
# 📌 PARAMETERIZED LOAN DECISION TESTS
# ================================
@pytest.mark.parametrize("test_case", [
    {
        "input": {"name": "Alice Johnson", "age": 40, "revenue": 120000, "credit_score": 780, "loan_amount": 25000},
        "expected": "Approved"
    },
    {
        "input": {"name": "Bob Smith", "age": 32, "revenue": 45000, "credit_score": 600, "loan_amount": 30000},
        "expected": "Rejected"
    },
    {
        "input": {"name": "Charlie Brown", "age": 29, "revenue": 90000, "credit_score": 720, "loan_amount": 20000},
        "expected": "Rejected"
    }
])
def test_end_to_end_loan_decisions(start_api, test_case):
    """
    📊 Sends real-world loan applications and validates underwriting decisions.
    """
    response = requests.post(f"{BASE_URL}/evaluate_loan", json=test_case["input"])
    assert response.status_code == 200, "API did not respond with HTTP 200!"
    data = response.json()
    assert test_case["expected"] in data["loan_decision"], "Unexpected loan decision outcome!"

# ================================
# 📏 STRESS TEST: LARGE PAYLOAD HANDLING
# ================================
def test_large_payload_handling(start_api):
    """
    🏋️‍♂️ Tests how the system handles extremely large payloads.
    """
    large_payload = {
        "name": "Test User",
        "age": 45,
        "revenue": 10000000,
        "credit_score": 800,
        "loan_amount": 100000000,
        "extra_data": "x" * 50000  # Simulate oversized payload 🛑
    }
    response = requests.post(f"{BASE_URL}/evaluate_loan", json=large_payload)
    assert response.status_code in [200, 400, 413], "API did not handle large payload correctly!"

# ================================
# ❌ ERROR HANDLING TEST
# ================================
def test_system_error_handling(start_api):
    """
    ⚠️ Ensures the API correctly handles invalid input and errors.
    """
    invalid_payload = {"name": "Test", "age": "NaN", "revenue": -5000}  # Invalid values 🚨
    response = requests.post(f"{BASE_URL}/evaluate_loan", json=invalid_payload)
    assert response.status_code == 400, "API should return HTTP 400 for invalid inputs!"



# ================================
# 🚦 API SHUTDOWN TEST
# ================================
def test_api_shutdown_gracefully(start_api):
    """
    🛑 Ensures the API shuts down properly without leaving orphaned processes.
    """
    logger.info("Shutting down API...")
    start_api.terminate()
    start_api.wait(timeout=5)
    kill_process_on_port(5000)
    logger.info("API shut down successfully.")
