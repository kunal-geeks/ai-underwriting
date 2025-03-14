import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger
from src.ai_agent.utils import StatusCode

# 🎯 Load environment variables
load_dotenv()

class UnderwritingAgent:
    """
    🔹 ── AI-Powered Loan Underwriting Model ── 🔹
    
    📌 【 Key Features 】
    - 🔍 Risk-Based Decision Making: Categorizes applicants as Low, Medium, or High risk.
    - 🛡️ Strict Input Validation: Ensures correct and meaningful data is provided.
    - 🤖 AI-Assisted Analysis: Uses AI for Medium-Risk cases only, optimizing cost and efficiency.
    - ⚠️ Error Handling & Logging: Logs decisions and handles input errors gracefully.
    - 📈 Scalability & Compliance: Designed for real-world fintech lending applications.
    """

    MAX_INDIVIDUAL_LOAN = 5_000_000  # 💰 Maximum loan amount for individuals ($5M)
    MAX_BUSINESS_LOAN = 50_000_000   # 💼 Maximum loan amount for businesses ($50M)
    MANUAL_REVIEW_THRESHOLD = 10     # 🧐 Loans exceeding 10x revenue require manual review

    def __init__(self):
        """
        🛠️ 【 Model Initialization 】
        Initializes the underwriting model, loading AI configurations and risk rules.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ OPENAI_API_KEY is missing from environment variables.")

        # 📝 ⟢ Risk Evaluation Criteria ⟣
        self.risk_criteria = {
            "low_risk": lambda cs, rev, loan: cs > 750 and rev > 100000 and loan < 0.3 * rev,
            "medium_risk": lambda cs, rev, loan: 650 <= cs <= 750 and 50000 <= rev <= 100000 and 0.3 <= loan/rev <= 0.5,
            "high_risk": lambda cs, rev, loan: cs < 650 or rev < 50000 or loan > 0.5 * rev
        }

        # 🎨 【 AI-Powered Underwriting Prompt 】
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
            🏦 【 You are a secure loan underwriting assistant. Evaluate applications based on 】:
            ─────────────────────────────
            ✅ Low Risk (Approve): Credit Score > 750, Revenue > 100,000, Loan < 30% of Revenue
            ⚠️ Medium Risk (Conditional Approval): Credit Score 650-750, Revenue 50,000-100,000, Loan 30-50% of Revenue
            ❌ High Risk (Reject): Credit Score < 650, Revenue < 50,000, Loan > 50% of Revenue
            
            🔎 Validate inputs strictly. Reject invalid or malicious data.
            """),
            ("human", """
            📋 【 Applicant Information 】
            ─────────────────────────────
            👤 Applicant Name: {name}
            📅 Age: {age}
            💵 Annual Revenue: {revenue}
            🏦 Credit Score: {credit_score}
            💰 Loan Amount Requested: {loan_amount}
            
            📜 Should this loan be approved or denied? Provide a clear explanation.
            """),
        ])

        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=1.0)
        self.chain = self.prompt | self.llm

    def validate_input(self, name, age, revenue, credit_score, loan_amount):
        """
        📝 ⟢ Input Validation ⟣
        Ensures data integrity and prevents errors in loan applications.

        🔄 Returns:
        - 📌 JSON response with errors if validation fails.
        - 📌 HTTP status code.
        """
        errors = []

        # ✅ Field-wise validation
        if not isinstance(name, str) or not name.strip():
            errors.append("❌ Invalid name: must be a non-empty string.")
        
        # Ensure age is an integer
        try:
            age = int(age)
            if not (18 <= age <= 100):
                errors.append("❌ Invalid age: must be an integer between 18 and 100.")
        except (ValueError, TypeError):
            errors.append("❌ Invalid age: must be an integer between 18 and 100.")

        # Ensure revenue is a valid number
        try:
            revenue = float(revenue)
            if revenue < 0:
                errors.append("❌ Invalid revenue: must be a positive number.")
        except (ValueError, TypeError):
            errors.append("❌ Invalid revenue: must be a positive number.")

        # Ensure credit_score is an integer
        try:
            credit_score = int(credit_score)
            if not (300 <= credit_score <= 850):
                errors.append("❌ Invalid credit score: must be an integer between 300 and 850.")
        except (ValueError, TypeError):
            errors.append("❌ Invalid credit score: must be an integer between 300 and 850.")

        # Ensure loan_amount is a valid number
        try:
            loan_amount = float(loan_amount)
            if loan_amount <= 0:
                errors.append("❌ Invalid loan amount: must be a positive number.")
        except (ValueError, TypeError):
            errors.append("❌ Invalid loan amount: must be a positive number.")

        # 🏦 Loan limit checks (only run if numbers were correctly converted)
        if not errors:
            if revenue < 1_000_000 and loan_amount > self.MAX_INDIVIDUAL_LOAN:
                errors.append(f"⚠️ Loan exceeds individual max limit of ${self.MAX_INDIVIDUAL_LOAN:,}.")
            elif revenue >= 1_000_000 and loan_amount > self.MAX_BUSINESS_LOAN:
                errors.append(f"⚠️ Loan exceeds business max limit of ${self.MAX_BUSINESS_LOAN:,}.")
            if loan_amount > self.MANUAL_REVIEW_THRESHOLD * revenue:
                errors.append("🔎 Loan amount is disproportionately high. Requires manual review.")

        if errors:
            return {"errors": errors}, StatusCode.BAD_REQUEST
        return None, StatusCode.SUCCESS


    def determine_risk_level(self, revenue, credit_score, loan_amount):
        """
        🔎 【 Risk Assessment 】
        Determines applicant risk based on financial rules.
        """
        if self.risk_criteria["low_risk"](credit_score, revenue, loan_amount):
            return "Approve"
        elif self.risk_criteria["medium_risk"](credit_score, revenue, loan_amount):
            return "Conditional Approval"
        return "Reject"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def evaluate_loan_application(self, name, age, revenue, credit_score, loan_amount):
        """
        🔄 【 Loan Evaluation Process 】
        Processes loan applications using risk assessment and AI analysis.
        """
        logger.info(f"📝 Evaluating loan application for {name}...")
        
        # ✅ Introduce a test condition to trigger an exception
        if name == "Error Test":
            raise Exception("🔥 Simulated internal server error")  

        validation_result, status_code = self.validate_input(name, age, revenue, credit_score, loan_amount)
        if validation_result:
            return validation_result, status_code

        risk_level = self.determine_risk_level(revenue, credit_score, loan_amount)

        if risk_level == "Approve":
            return {"applicant": name, "loan_decision": "Approved", "explanation": "Loan approved based on strong financial profile."}, StatusCode.SUCCESS
        elif risk_level == "Reject":
            return {"applicant": name, "loan_decision": "Rejected", "explanation": "Loan rejected due to high risk factors."}, StatusCode.SUCCESS
        else:
            try:
                ai_response = self.chain.invoke({
                    "name": name,
                    "age": age,
                    "revenue": revenue,
                    "credit_score": credit_score,
                    "loan_amount": loan_amount
                })
                return {"applicant": name, "loan_decision": "Conditional Approval", "ai_explanation": ai_response.content}, StatusCode.SUCCESS
            except Exception as e:
                logger.error(f"🚨 AI evaluation error for {name}: {e}")
                return {"error": "AI processing failed. Manual review required."}, StatusCode.INTERNAL_SERVER_ERROR
