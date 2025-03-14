# 🏦 AI-Powered Underwriting System

## 📌 Overview
An AI-powered underwriting API that automates credit risk assessment. It evaluates loan eligibility based on credit scores, income, and requested loan amounts.

---

## 🚀 Features
✅ AI-driven underwriting decisions  
✅ API-based credit risk assessment  
✅ Bias and security testing  
✅ Fully containerized using Docker & Redis  
✅ CI/CD pipeline with GitHub Actions  

---

## 🛠️ Tech Stack & Frameworks

| Technology    | Purpose                          |
|--------------|---------------------------------|
| 🐍 **Python**  | Core language for AI and testing  |
| 🧪 **PyTest**  | Unit, integration, and fairness testing |
| 🌐 **Flask**  | Mock AI API & endpoints |
| 🤖 **LangChain**  | Testing LLM-based AI agents |
| 🎯 **Celery**  | Async test execution |
| 🐳 **Docker**  | Containerized test environments |
| 🔄 **Jenkins**  | CI/CD integration |
| 📬 **Postman/Newman**  | API testing |
| 🚀 **GitHub Actions**  | CI/CD pipeline |
| 📊 **Locust**  | Performance testing |

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
 git clone https://github.com/kunal-geeks/ai-underwriting.git
 cd ai-underwriting
```

### 2️⃣ Run with Docker Compose

🔹 **Create a `.env` file** inside the `docker` folder and add your `OPENAI_API_KEY` before proceeding.

🔹 **Rebuild the image without cache:**
```bash
docker compose -f docker/docker-compose-local.yml --env-file .env build --no-cache
```

🔹 **Start the containers:**
```bash
docker compose -f docker/docker-compose-local.yml --env-file .env up
```

🔹 **Stop the containers:**
```bash
docker compose -f docker/docker-compose-local.yml --env-file .env down
```

🌍 The API will be available at: `http://underwriting_app_local:5001`

---

## ✅ Run Tests
📌 Tests will run automatically inside Docker, and reports will be generated inside the `reports` folder.

---

## 📊 Run Performance Tests with Locust

To start **performance testing** using Locust, run the following command:
```bash
locust -f src/tests/api/non-functional/performance/locustfile.py --host=http://127.0.0.1:5001
```

Once Locust is running, open your browser and go to:
📌 **http://127.0.0.1:8089** to start the test.

---

## 🔗 API Endpoints

### 🚀 Underwrite Loan Request
#### **POST** `/evaluate_loan`
📩 **Request:**
```json
{
  "name": "Bob Williams",
  "age": 42,
  "revenue": 80000,
  "credit_score": 700,
  "loan_amount": 35000
}
```

✅ **Response:**
```json
{
  "ai_explanation": "To evaluate Bob Williams' loan application, let's assess the provided data against the defined criteria:\n\n- **Credit Score**: 700\n- **Annual Revenue**: $80,000\n- **Loan Amount Requested**: $35,000\n\nSince Bob's credit score and revenue fall into the Medium Risk category and the loan amount requested is also within the acceptable range for this category:\n\n**Decision**: Medium Risk (Conditional Approval)\n\n**Explanation**: Bob Williams meets the criteria for a Medium Risk application. The recommended action is to issue a **conditional approval** for the loan, possibly requiring additional documentation.",
  "applicant": "Bob Williams",
  "loan_decision": "Conditional Approval"
}
```

📩 **Request:**
```json
{
  "name": "Charlie Brown",
  "age": 29,
  "revenue": 40000,
  "credit_score": 600,
  "loan_amount": 25000
}
```

❌ **Response:**
```json
{
  "applicant": "Charlie Brown",
  "explanation": "Loan rejected due to high risk factors.",
  "loan_decision": "❌ Rejected"
}
```

---

## 🚀 CI/CD Pipeline with GitHub Actions
✅ **Steps:**
- Configure GitHub Actions.
- Add `prod_deploy.yml` file to automate testing & deployment.

---

## 🎯 Conclusion
The AI-powered underwriting system provides a robust, scalable, and automated approach to loan risk assessment. With a strong focus on fairness, security, and performance, this project is set to revolutionize AI-driven lending. 🚀💰

---

## 📌 Author
🔹 **Kunal Geeks**  
💻 [GitHub](https://github.com/kunal-geeks) | 🐦 [Twitter](https://twitter.com/kunalgeeks) | 📧 Email: kunal@geeks.dev

