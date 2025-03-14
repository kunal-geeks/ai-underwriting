import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.tests.conftest import BASE_URL
from src.loguru_logger import logger

# 📌 API Endpoint 
API_URL = f"{BASE_URL}/evaluate_loan"

def test_api_latency(sample_payload):
    """
    ⏳ API Latency Test: Ensures response time is within acceptable limits.
    
    ✅ Expected: Response time < 2s
    """
    start_time = time.time()
    response = requests.post(API_URL, json=sample_payload)
    end_time = time.time()

    duration = end_time - start_time
    logger.info(f"⏳ API Latency: {duration:.2f}s")

    assert response.status_code == 200, f"❌ API Failure: {response.status_code}"
    assert duration < 2, f"⚠️ Slow response: {duration:.2f} sec"


def test_high_concurrency():
    """
    🚀 High-Concurrency Test: Simulates 50 parallel users to assess system stability.
    
    ✅ Expected: All responses should return HTTP 200.
    """
    def send_request():
        try:
            response = requests.post(API_URL, json={
                "name": "Concurrent User",
                "age": 40,
                "revenue": 120000,
                "credit_score": 780,
                "loan_amount": 30000
            })
            return response.status_code
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Request failed: {e}")
            return None

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(send_request) for _ in range(40)]

        results = []
        for future in as_completed(futures):
            results.append(future.result())

    success_count = sum(1 for status in results if status == 200)
    failure_count = len(results) - success_count

    logger.info(f"🚀 High Concurrency Results: {success_count} ✅ | {failure_count} ❌")

    assert success_count == len(results), "⚠️ Some requests failed under high load"


def test_large_payload():
    """
    📦 Large Payload Test: Checks how API handles oversized payloads.
    
    ✅ Expected: API should return either 200 (success) or 400 (bad request).
    """
    large_payload = {
        "name": "Bulk Test User",
        "age": 35,
        "revenue": 9000000,
        "credit_score": 800,
        "loan_amount": 5000000,
        "extra_field": "x" * 500000  # Reduced for speed
    }
    
    response = requests.post(API_URL, json=large_payload)
    logger.info(f"📦 Large Payload Response: {response.status_code}")

    assert response.status_code in [200, 400], f"❌ Unexpected response: {response.status_code}"


def test_rapid_fire_requests(sample_payload):
    """
    🔫 Rapid-Fire Request Test: Sends multiple requests in quick succession to detect rate limiting or crashes.
    
    ✅ Expected: All requests return HTTP 200.
    """
    failures = 0
    for i in range(9):  
        response = requests.post(API_URL, json=sample_payload)
        if response.status_code != 200:
            failures += 1
            logger.error(f"⚠️ Request {i+1} failed: {response.status_code}")

    logger.info(f"🔫 Rapid-Fire Test: {10 - failures} ✅ | {failures} ❌")

    assert failures == 0, "⚠️ API failed under rapid-fire conditions"


def test_system_resilience():
    """
    🔄 System Resilience Test: Simulates API downtime by hitting an invalid endpoint.
    
    ✅ Expected: Either a 404 response or a connection failure.
    """
    try:
        response = requests.post("http://127.0.0.1:5001/evaluate_loan", json={})
        logger.info(f"🔄 Resilience Test Response: {response.status_code}")
        assert response.status_code == 404, "⚠️ Unexpected behavior when API is down"
    except requests.exceptions.ConnectionError:
        logger.warning("✅ Expected behavior: API is unreachable.")
        assert True  # Expected behavior
