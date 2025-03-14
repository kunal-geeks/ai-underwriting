import os
import random
import json
from dotenv import load_dotenv
from faker import Faker
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

AI_OUTPUT_FILE = "generated_data/ai_generated_financial_document.json"

# Load environment variables
load_dotenv()

fake = Faker()

class SyntheticDataGenerator:
    def __init__(self):
        """
        Initializes the synthetic data generator with AI-driven test case expansion.
        """
        api_key = os.getenv("OPENAI_API_KEY")  # Get API key from environment
        if not api_key:
            raise ValueError("Missing OpenAI API key. Set the OPENAI_API_KEY environment variable.")
        
        # Initialize OpenAI Chat Model
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=1.0)

        # Create a prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Generate a realistic and detailed financial document based on the given parameters."),
            ("human", "Generate a financial document with the following details: Credit Score: {credit_score}, Revenue: {revenue}, Loan Amount: {loan_amount}.")
        ])

        # Chain the prompt with LLM to ensure correct execution
        self.chain = self.prompt | self.llm | RunnableLambda(lambda x: x.content if hasattr(x, "content") else str(x))

    def generate_loan_application(self):
        """
        Generates a synthetic loan application with realistic data.
        """
        credit_score = random.randint(500, 850)
        revenue = random.randint(20000, 200000)
        loan_amount = random.randint(5000, 50000)
        
        application = {
            "name": fake.name(),
            "age": random.randint(21, 65),
            "revenue": revenue,
            "credit_score": credit_score,
            "loan_amount": loan_amount
        }
        
        return application
    
    def generate_financial_document(self):
        """
        Generates a mock financial document as JSON.
        """
        document = {
            "business_name": fake.company(),
            "annual_revenue": random.randint(50000, 500000),
            "expenses": random.randint(10000, 300000),
            "profit": random.randint(5000, 200000),
            "credit_score": random.randint(500, 850)
        }
        return json.dumps(document, indent=4)
    
    def generate_bulk_applications(self, n=10):
        """
        Generates multiple synthetic loan applications.
        """
        return [self.generate_loan_application() for _ in range(n)]
    
    def generate_ai_test_case(self, credit_score, revenue, loan_amount, save_to_file=True):
        """
        Generates an AI-based financial document and optionally saves it to a file.
        """
        response = self.chain.invoke({
            "credit_score": credit_score,
            "revenue": revenue,
            "loan_amount": loan_amount
        })

        ai_response = response.content if hasattr(response, "content") else str(response)

        # Save response to a JSON file if enabled
        if save_to_file:
            ai_data = {
                "input": {
                    "credit_score": credit_score,
                    "revenue": revenue,
                    "loan_amount": loan_amount
                },
                "generated_document": ai_response
            }
            with open(AI_OUTPUT_FILE, "w", encoding="utf-8") as file:
                json.dump(ai_data, file, indent=4)

        return ai_response

    def load_ai_test_case(self):
        """
        Loads the AI-generated financial document from a file.
        """
        if not os.path.exists(AI_OUTPUT_FILE):
            raise FileNotFoundError(f"{AI_OUTPUT_FILE} not found. Run generate_ai_test_case first.")

        with open(AI_OUTPUT_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

if __name__ == "__main__":
    generator = SyntheticDataGenerator()
    
    # Generate and print a sample loan application
    print("Sample Loan Application:")
    print(json.dumps(generator.generate_loan_application(), indent=4))
    
    # Generate and print a sample financial document
    print("\nSample Financial Document:")
    print(generator.generate_financial_document())
    
    # Generate an AI-based test case (real-world financial document)
    print("\nAI-Generated Financial Document:")
    print(generator.generate_ai_test_case(700, 80000, 20000))
