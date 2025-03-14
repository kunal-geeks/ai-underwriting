# AI-Powered Underwriting System

## Overview
This project is an AI-powered underwriting API that automates credit risk assessment. It evaluates loan eligibility based on credit scores, income, and requested loan amounts.

## Features
✅ AI-driven underwriting decisions  
✅ API-based credit risk assessment  
✅ Bias and security testing  
✅ Fully containerized using Docker & Redis  
✅ CI/CD pipeline with Github Actions.

## Tech Stack
- **Backend**: Python, Flask, Celery
- **Database**: Redis (for caching)
- **Testing**: PyTest, Security & Bias Testing
- **Containerization**: Docker & Docker-Compose
- **CI/CD**: Jenkins

## Setup Instructions
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/ai-underwriting.git
cd ai-underwriting
```

### 2️⃣ Run with Docker Compose
```bash
docker-compose up --build
```
The API will be available at `http://localhost:5000`

### 3️⃣ Run Tests
```bash
docker-compose exec underwriting-api pytest tests/
```

### 4️⃣ API Endpoints
#### Underwrite Loan Request
**POST** `/underwrite`
```json
{
  "cibil_score": 750,
  "income": 80000,
  "loan_amount": 50000
}
```
✅ **Response:**
```json
{
  "decision": "Approved"
}
```

### 5️⃣ CI/CD Pipeline with Jenkins
- Configure Jenkins with a GitHub webhook.
- Add Jenkinsfile to automate testing & deployment.

---
🚀 **Ready to revolutionize AI-driven lending!**
