import json
import random
from faker import Faker
from src.logger import get_logger

logger = get_logger()

class SyntheticDataGenerator:
    def __init__(self, num_cases=100):
        self.num_cases = num_cases
        self.fake = Faker()

    def generate_loan_application(self):
        """Generates a synthetic loan application."""
        return {
            "name": self.fake.name(),
            "age": random.randint(21, 65),
            "revenue": random.randint(30000, 200000),
            "credit_score": random.randint(300, 850),
            "loan_amount": random.randint(5000, 50000)
        }

    def determine_decision(self, application):
        """Determines the expected loan decision based on defined criteria."""
        if (application["credit_score"] > 750 and
            application["revenue"] > 100000 and
            application["loan_amount"] <= 0.3 * application["revenue"]):
            return "approve"
        elif (650 <= application["credit_score"] <= 750 and
              50000 <= application["revenue"] <= 100000 and
              0.3 * application["revenue"] < application["loan_amount"] <= 0.5 * application["revenue"]):
            return "conditional_approval"
        else:
            return "reject"

    def generate_test_cases(self):
        """Generates synthetic test cases with labeled decisions."""
        test_cases = []
        for _ in range(self.num_cases):
            application = self.generate_loan_application()
            decision = self.determine_decision(application)

            test_cases.append({
                "input": application,
                "expected": decision
            })

        output_path = "synthetic_test_cases.json"
        with open(output_path, "w") as f:
            json.dump(test_cases, f, indent=4)

        logger.info(f"Generated {self.num_cases} synthetic loan applications and saved to {output_path}.")

if __name__ == "__main__":
    generator = SyntheticDataGenerator(num_cases=100)
    generator.generate_test_cases()
