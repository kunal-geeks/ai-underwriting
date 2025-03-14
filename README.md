# AI-Powered Underwriting System

## Overview
This project is an AI-powered underwriting API that automates credit risk assessment. It evaluates loan eligibility based on credit scores, income, and requested loan amounts.

## Features
✅ AI-driven underwriting decisions  
✅ API-based credit risk assessment  
✅ Bias and security testing  
✅ Fully containerized using Docker & Redis  
✅ CI/CD pipeline with Github Actions.

## Tech Stack & Frameworks
✅ Python – Core language for AI and testing
✅ PyTest – Unit, integration testing, Bias detection, fairness testing
✅ Flask – Mock AI API & endpoints
✅ LangChain – Testing LLM-based AI agents
✅ Celery – Async test execution
✅ Docker – Containerized test environments
✅ Jenkins – CI/CD integration
✅ Postman / Newman – API testing
✅ CI/CD - Github Actions
✅ Locust - Performance testing  

## Setup Instructions
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/kunal-geeks/ai-underwriting.git
cd ai-underwriting
```

### 2️⃣ Run with Docker Compose

- create a .env file inside the docker folder and add your OPENAI_API_KEY before proceeding

- Rebuild the image without cache:
```bash
docker compose -f docker/docker-compose-local.yml --env-file .env build --no-cache
```
- Start the containers:
```bash
docker compose -f docker/docker-compose-local.yml --env-file .env up
```
- Stop the containers:
```bash
docker compose -f docker/docker-compose-local.yml --env-file .env down
```
The API will be available at `http://underwriting_app_local:5001`

### 3️⃣ Run Tests
```bash
Tests will run automatically run inside docker and reports will be generated inside reports folder.
```

### 4️⃣ API Endpoints
#### Underwrite Loan Request
**POST** `/evaluate_loan`

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
	"ai_explanation": "To evaluate Bob Williams' loan application, let's assess the provided data against the defined criteria:\n\n- **Credit Score**: 700\n- **Annual Revenue**: $80,000\n- **Loan Amount Requested**: $35,000\n\n1. **Credit Score**: Bob's credit score is 700, which falls within the Medium Risk category since it is between 650 and 750.\n  \n2. **Annual Revenue**: His annual revenue is $80,000, which is also within the Medium Risk range (between $50,000 and $100,000).\n\n3. **Loan Amount as a Percentage of Revenue**: To determine eligibility based on the loan amount, we calculate the percentage:\n   \\[\n   \\text{Loan Percentage} = \\left(\\frac{\\text{Loan Amount}}{\\text{Annual Revenue}} \\times 100\\right) = \\left(\\frac{35000}{80000} \\times 100\\right) = 43.75\\%\n   \\]\n   This percentage indicates that the loan amount requested is 43.75% of the annual revenue, which is between 30% and 50%.\n\nSince Bob's credit score and revenue fall into the Medium Risk category and the loan amount requested is also within the acceptable range for this category:\n\n**Decision**: Medium Risk (Conditional Approval)\n\n**Explanation**: Bob Williams meets the criteria for a Medium Risk application. The recommended action is to issue a **conditional approval** for the loan, possibly requiring additional documentation or factors to be considered before final approval.",
	"applicant": "Bob Williams",
	"loan_decision": "Conditional Approval"
  },
  200



{
  "name": "Charlie Brown",
  "age": 29,
  "revenue": 40000,
  "credit_score": 600,
  "loan_amount": 25000
}

```
✅ **Response:**
```json

 {
	"applicant": "Charlie Brown",
	"explanation": "Loan rejected due to high risk factors.",
	"loan_decision": "\u274c Rejected"
  },
  200

```

### 5️⃣ CI/CD Pipeline with Github Actions
- Configure GitHub Actions.
- Add prod_deploy.yml file to automate testing & deployment.

---
🚀 **Ready to revolutionize AI-driven lending!**
