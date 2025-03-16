# AI-Powered Testing Automation for AI Agents in Fintech

## 📌 Project Description

This project introduces an industry-level AI-driven test automation system designed specifically for testing AI agents utilized in fintech lending. The system focuses on validating AI models, large language models (LLMs), APIs, and risk assessment workflows to ensure accuracy, fairness, security, and reliability.

With AI playing a crucial role in underwriting, credit scoring, and fraud detection, our framework automates testing processes to detect model biases, security vulnerabilities, and performance bottlenecks. The automation pipeline leverages AI-powered test case generation, adversarial testing, and CI/CD integration to maintain robust and high-quality AI systems.

## 🚀 Key Features

✅ **AI-Driven Test Automation** - Automates the testing of AI models, APIs, and underwriting workflows.
✅ **Automated API Testing** - Validates AI-powered APIs with functional, integration, and performance tests.
✅ **Bias and Fairness Testing** - Ensures AI models provide unbiased credit decisions and risk assessments.
✅ **Prompt Injection & Security Testing** - Simulates malicious inputs to test robustness against AI vulnerabilities.
✅ **Self-Healing Test Cases** - AI-driven auto-correction of failed test cases.
✅ **CI/CD Pipeline with GitHub Actions** - Fully automated testing and deployment process.
✅ **Containerized Deployment** - Runs in a Dockerized environment with cloud integration.
✅ **Performance & Load Testing** - Uses Locust for high-volume testing and response time validation.

This AI-powered testing framework ensures the reliability and fairness of AI agents used in fintech, helping lenders make data-driven and ethical loan decisions. 🚀💰

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
| 💌 **Postman/Newman**  | API testing |
| 🚀 **GitHub Actions**  | CI/CD pipeline |
| 📊 **Locust**  | Performance testing |

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
 git clone https://github.com/kunal-geeks/ai-underwriting.git
 cd ai-underwriting
```

### 2️⃣ Run with Docker Compose (On Your Local Machine)

🔹 **Create a `.env` file** inside the `docker` folder and add your `OPENAI_API_KEY` before proceeding.

#### 💻 For **MacOS/Linux:**
```bash
docker compose -f docker/docker-compose-local.yml --env-file .env build --no-cache
```
```bash
docker compose -f docker/docker-compose-local.yml --env-file .env up
```
```bash
docker compose -f docker/docker-compose-local.yml --env-file .env down
```
```bash
docker compose -f docker/docker-compose-local.yml up --build --force-recreate
```
✅ This command **rebuilds** the containers from scratch and **forces recreation** to apply all dependencies and configurations.

#### 🖥️ For **Windows (PowerShell):**
```powershell
docker-compose -f docker/docker-compose-local.yml --env-file .env build --no-cache
```
```powershell
docker-compose -f docker/docker-compose-local.yml --env-file .env up
```
```powershell
docker-compose -f docker/docker-compose-local.yml --env-file .env down
```
```powershell
docker-compose -f docker/docker-compose-local.yml up --build --force-recreate
```
🌍 The API will be available at: `http://underwriting_app_local:5001`

---

## ✅ Run Tests
📌 Tests will run automatically inside Docker, and reports will be generated inside the `reports` folder.

---

## 📊 Run Performance Tests with Locust (On Your Local Machine)

To start **performance testing** using Locust:

- First start the flask server locally by following command:
```bash
  poetry run python src/app.py
```
🌍 The API will be available at: `http://127.0.0.1:5001`

#### 💻 For **MacOS/Linux:**
```bash
locust -f src/tests/api/non-functional/performance/locustfile.py --host=http://127.0.0.1:5001
```
#### 🖥️ For **Windows (PowerShell):**
```powershell
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
  "ai_explanation": "Loan decision explanation...",
  "applicant": "Bob Williams",
  "loan_decision": "Conditional Approval"
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
🔹 **Kunal Sharma**  
💻 [GitHub](https://github.com/kunal-geeks) | 🐦 [Twitter](https://x.com/kunal_ucet) | 📧 Email: kunal.sdet001@gmail.com

