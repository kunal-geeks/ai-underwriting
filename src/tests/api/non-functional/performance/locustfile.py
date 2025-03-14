from locust import HttpUser, task, between

class LoanEvaluationUser(HttpUser):
    wait_time = between(1, 3)  # Users wait between 1 and 3 seconds before sending the next request

    @task(3)
    def evaluate_loan_standard(self):
        """Simulates a standard loan evaluation request."""
        self.client.post("/evaluate_loan", json={
            "name": "Test User",
            "age": 35,
            "revenue": 90000,
            "credit_score": 720,
            "loan_amount": 20000
        })

    @task(2)
    def evaluate_loan_high_risk(self):
        """Simulates a loan request with high-risk profile."""
        self.client.post("/evaluate_loan", json={
            "name": "High Risk",
            "age": 50,
            "revenue": 40000,
            "credit_score": 600,
            "loan_amount": 50000
        })

    @task(1)
    def stress_test(self):
        """Simulates a high-load scenario."""
        for _ in range(10):
            self.client.post("/evaluate_loan", json={
                "name": "Stress Test",
                "age": 40,
                "revenue": 100000,
                "credit_score": 750,
                "loan_amount": 25000
            })
