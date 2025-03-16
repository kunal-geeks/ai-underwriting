# AI-Powered Testing Automation for AI Agents in Fintech

## 📌 Project Description

This project introduces an industry-level AI-driven test automation system designed specifically for testing AI agents utilized in fintech lending. The system focuses on validating AI models, large language models (LLMs), APIs, and risk assessment workflows to ensure accuracy, fairness, security, and reliability.

With AI playing a crucial role in underwriting, credit scoring, and fraud detection, our framework automates testing processes to detect model biases, security vulnerabilities, and performance bottlenecks. The automation pipeline leverages AI-powered test case generation, adversarial testing, and CI/CD integration to maintain robust and high-quality AI systems.

## 🚀 Key Features

👉 **AI-Driven Test Automation** - Automates the testing of AI models, APIs, and underwriting workflows.  
👉 **Automated API Testing** - Validates AI-powered APIs with functional, integration, and performance tests.  
👉 **Bias and Fairness Testing** - Ensures AI models provide unbiased credit decisions and risk assessments.  
👉 **Prompt Injection & Security Testing** - Simulates malicious inputs to test robustness against AI vulnerabilities.  
👉 **Self-Healing Test Cases** - AI-driven auto-correction of failed test cases.  
👉 **CI/CD Pipeline with GitHub Actions** - Fully automated testing and deployment process.  
👉 **Containerized Deployment** - Runs in a Dockerized environment.  
👉 **Performance & Load Testing** - Uses Locust for high-volume testing and response time validation.  
👉 **Nginx as Reverse Proxy for Security** -  Enhances security and scalability by forwarding traffic securely to backend services.  

This AI-powered testing framework ensures the reliability and fairness of AI agents used in fintech, helping lenders make data-driven and ethical loan decisions. 🚀💰

---

## 🛠️ Tech Stack & Frameworks

| Technology    | Purpose                          |
|--------------|---------------------------------|
| 🐍 **Python**  | Core language for AI and testing  |
| 🤪 **PyTest**  | Unit, integration, and fairness testing |
| 🌐 **Flask**  | Mock AI API & endpoints |
| 🤖 **LangChain**  | Testing LLM-based AI agents |
| 🎯 **Celery**  | Async test execution |
| 🐋 **Docker**  | Containerized test environments |
| 📩 **Postman/Newman**  | API testing |
| 🚀 **GitHub Actions**  | CI/CD pipeline |
| 📊 **Locust**  | Performance testing |
| 🛡 **Nginx**  | Reverse proxy & security |

---

## 📂 Project Folder Structure (Blueprint)

```
ai-underwriting/
├── .github/
│   ├── workflows/
│   │   ├── prod_deploy.yml   # CI/CD deployment workflow for production
├── docs/                     # Project documentation
│   └── design.md             # Design and architecture decisions
├── config/                   # Configuration files for different environments
│   ├── dev/                  # Development configuration
│   │   ├── config.yml        # Dev environment config
│   ├── prod/                 # Production configuration
│   │   ├── config.yml        # Production environment config
│   ├── qa/                   # QA environment configuration
│   │   ├── config.yml        # QA environment config
│   ├── nginx/                # Nginx configuration for reverse proxy and SSL
│   │   ├── ssl/              # SSL certificates
│   │   │   ├── nginx-selfsigned.crt  # Self-signed certificate
│   │   │   ├── nginx-selfsigned.key  # Self-signed private key
│   │   ├── nginx-local.conf  # Local Nginx configuration
│   │   ├── nginx.conf        # Production Nginx configuration
│   │   ├── gunicorn_config.py  # Gunicorn configuration
├── docker/                   # Docker configurations
│   ├── .env                  # Environment variables
│   ├── Dockerfile.dev        # Dockerfile for development environment
│   ├── Dockerfile.prod       # Dockerfile for production environment
│   ├── docker-compose-local.yml # Local Docker Compose configuration
│   ├── docker-compose-prod.yml # Production Docker Compose configuration
├── src/                      # Source code
│   ├── __init__.py           # Package initialization
│   ├── app.py                # Flask application entry point
│   ├── logger.py             # Logging utility
│   ├── loguru_logger.py      # Enhanced logging with Loguru
│   ├── setup.py              # Setup script for package installation
│   ├── pytest.ini            # Pytest configuration file
│   ├── api/                  # API-related files (Flask)
│   │   ├── __init__.py       # API entry point
│   │   ├── routes.py         # Define all API endpoints
│   │   └── config.py         # API-specific configurations (environment vars, secrets)
│   ├── ai_agent/             # AI model and agent-related code
│   │   ├── __init__.py       # AI agent initialization
│   │   ├── model.py          # AI model code (LangChain or similar)
│   │   ├── utils.py          # Helper functions (data preprocessing, post-processing)
│   ├── tests/                # Testing Framework
│       │── __init__.py             # Test package initialization
│       │── api/                    # API testing
│       │   │── __init__.py         # API test package initialization
│       │   │── functional/         # Functional tests
│       │   │   ├── __init__.py     # Functional test initialization
│       │   │   ├── unit/           # Unit tests
│       │   │   │   ├── __init__.py # Unit test initialization
│       │   │   │   ├── test_agent.py  # AI agent unit tests
│       │   │   │   ├── test_api.py    # API unit tests
│       │   │   ├── integration/    # Integration tests
│       │   │   │   ├── __init__.py # Integration test initialization
│       │   │   │   ├── test_api.py # API integration tests
│       │   │   ├── system/         # Full system tests
│       │   │   │   ├── __init__.py # System test initialization
│       │   │   │   ├── test_end_to_end.py # End-to-end system tests
│       │   │   ├── auto_test/      # AI-driven self-healing test cases
│       │   │       ├── __init__.py # Auto test initialization
│       │   │       ├── test_auto_test.py # AI-driven self-healing test cases
│       │   │── non-functional/     # Non-functional tests
│       │       ├── __init__.py     # Non-functional test initialization
│       │       ├── performance/    # Performance tests
│       │       │   ├── __init__.py # Performance test initialization
│       │       │   ├── test_performance.py # Performance testing
│       │       │   ├── locustfile.py # Load testing with Locust
│       │       ├── security/       # Security testing
│       │       │   ├── __init__.py # Security test initialization
│       │       │   ├── test_security.py # Security testing (prompt injection, vulnerabilities)
│       │       ├── fairness/       # Fairness & bias validation
│       │           ├── __init__.py # Fairness test initialization
│       │           ├── test_fairness.py # Bias and fairness validation
│       │── ui/                     # UI Testing
│           ├── __init__.py         # UI test initialization
├── reports/                  # Test reports and logs
├── Jenkinsfile               # CI/CD pipeline for Jenkins
├── README.md                 # Project overview and setup instructions
├── poetry.lock               # Poetry dependency lock file
├── pyproject.toml            # Python project configuration
```

---

## 🛠️ Setup Instructions

### 1⃣ Clone the Repository
```bash
git clone https://github.com/kunal-geeks/ai-underwriting.git
cd ai-underwriting
```

### 2⃣ Run with Docker Compose (On Your Local Machine)

🔹 **Create a `.env` file** inside the `docker` folder and add your `OPENAI_API_KEY` before proceeding.

#### 💻 For **MacOS/Linux:**
🔹 Use this command to build Docker images from scratch, ignoring cached layers, ensuring all dependencies and changes are applied.
```bash
docker compose -f docker/docker-compose-local.yml --env-file .env build --no-cache
```
🔹 Use this command to start all services defined in docker-compose-local.yml, loading environment variables from the .env file.
```bash
docker compose -f docker/docker-compose-local.yml --env-file .env up
```
🔹 Use this command to stop and remove all running containers, networks, and volumes created by docker compose up.
```bash
docker compose -f docker/docker-compose-local.yml --env-file .env down
```
🔹 Use this command to rebuild images and recreate all containers from scratch, ensuring the latest changes are applied.
```bash
docker compose -f docker/docker-compose-local.yml up --build --force-recreate
```

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

First start the Flask server locally by running the following command:
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
  "loan_decision": "Rejected"
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
💻 [GitHub](https://github.com/kunal-geeks) | 🕊 [Twitter](https://x.com/kunal_ucet) | 📧 Email: kunal.sdet001@gmail.com

