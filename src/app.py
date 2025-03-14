import signal
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis
import os
import yaml
from src.loguru_logger import logger  # Import centralized Loguru logger
from api.routes import register_routes

# Load configuration
ENV = os.getenv("APP_ENV", "dev")
CONFIG_PATH = f"config/{ENV}/config.yaml"

if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(f"Configuration file {CONFIG_PATH} not found!")

with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow CORS

# Configure Redis for Rate Limiting
try:
    redis_connection = Redis.from_url(config["redis"]["url"], decode_responses=True)
    redis_connection.ping()
    logger("✅ Connected to Redis successfully!")
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    redis_connection = None

limiter = Limiter(
    key_func=get_remote_address,  # Limits applied per user/IP
    storage_uri=config["redis"]["url"],  
    app=app,
    default_limits=["1000 per minute"],  # Adjusted general limit
)

# Apply Flask configuration
app.config.update(config["app"])

logger.info(f"🚀 Starting Flask app in {ENV} environment...")

# Register API routes
register_routes(app)

def shutdown_handler(signum, frame):
    """Log and clean up before API shuts down."""
    logger.info("🔥 API is shutting down gracefully...")
    exit(0)

# ✅ Register signal handlers for graceful shutdown
signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint with logging."""
    logger.info(f"✅ Health check requested from {request.remote_addr}")
    try:
        return jsonify({"message": "API is running", "status": "healthy"}), 200
    except Exception as e:
        logger.error(f"❌ Error in health check: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# 📌 Middleware to add security headers globally
@app.after_request
def add_security_headers(response):
    """
    🛡️ Injects security headers into all API responses globally.
    """
    response.headers["X-Frame-Options"] = "DENY"  # Prevents Clickjacking
    response.headers["Content-Security-Policy"] = "default-src 'self'"  # Restricts content sources
    response.headers["X-Content-Type-Options"] = "nosniff"  # Prevents MIME-type sniffing
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"  # Enforces HTTPS
    return response

    
if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":  # Prevent duplicate logs in dev mode
        logger.info("🔄 Running Flask server...")
    
    try:
        app.run(host=config["app"]["host"], port=config["app"]["port"], debug=config["app"]["debug"])
    except Exception as e:
        logger.error(f"🔥 Failed to start Flask server: {e}")
