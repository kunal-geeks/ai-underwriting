import os
from flask import request, jsonify
from ai_agent.model import UnderwritingAgent
from src.loguru_logger import logger
from src.ai_agent.utils import StatusCode
from werkzeug.exceptions import BadRequest

REQUIRED_FIELDS = {"name", "age", "revenue", "credit_score", "loan_amount"}

def register_routes(app):
    """
    Register all API routes with the Flask app.
    """
    underwriting_agent = UnderwritingAgent()

    @app.route('/health', methods=['GET'])
    def health_check():
        """
        API health check endpoint.
        """
        return jsonify({"status": "healthy", "message": "API is running"}), StatusCode.SUCCESS

    @app.route('/evaluate_loan', methods=['POST'])
    def evaluate_loan():
        """
        API endpoint to evaluate a loan application.
        """
        try:
            # Ensure valid JSON request
            try:
                data = request.get_json(force=True)
                if not isinstance(data, dict):
                    return jsonify({"error": "Invalid JSON format"}), StatusCode.BAD_REQUEST
            except BadRequest:
                return jsonify({"error": "Malformed JSON"}), StatusCode.BAD_REQUEST

            # Check for missing required fields
            missing_fields = [field for field in REQUIRED_FIELDS if field not in data]
            if missing_fields:
                logger.error(f"Missing fields in request: {missing_fields}")
                return jsonify({"errors": [f"Missing {field}" for field in missing_fields]}), StatusCode.BAD_REQUEST

            # Reject requests with unexpected extra fields
            extra_fields = [field for field in data.keys() if field not in REQUIRED_FIELDS]
            if extra_fields:
                return jsonify({"error": f"Unexpected fields: {', '.join(extra_fields)}"}), StatusCode.BAD_REQUEST

            # Call underwriting agent with validated input
            response, status_code = underwriting_agent.evaluate_loan_application(
                name=data["name"],
                age=data["age"],
                revenue=data["revenue"],
                credit_score=data["credit_score"],
                loan_amount=data["loan_amount"]
            )

            return jsonify(response), status_code

        except Exception as e:
            logger.error(f"🚨Error processing loan evaluation: {e}", exc_info=True)
            return jsonify({"error": "Internal server error"}), StatusCode.INTERNAL_SERVER_ERROR
        
    @app.route('/test_openai', methods=['GET'])
    def test_openai():
        """
        API endpoint to test OpenAI integration.
        """
        try:
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OpenAI API key is missing. Set it in your environment.")

            response = underwriting_agent.test_openai_integration()
            return jsonify({"status": "success", "response": response}), StatusCode.SUCCESS

        except Exception as e:
            logger.error(f"OpenAI API Error: {e}")
            return jsonify({"status": "error", "message": "Failed to connect to OpenAI"}), StatusCode.INTERNAL_SERVER_ERROR
        
    # 📌 Middleware to add security headers
    @app.after_request
    def add_security_headers(response):
        """
        🛡️ Injects security headers into all API responses.
        """
        response.headers["X-Frame-Options"] = "DENY"  # Prevents Clickjacking
        response.headers["Content-Security-Policy"] = "default-src 'self'"  # Restricts content sources
        response.headers["X-Content-Type-Options"] = "nosniff"  # Prevents MIME-type sniffing
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"  # Enforces HTTPS
        return response
