import os
import sys
import yaml
import logging
from loguru import logger
from flask import request  # Required for capturing request context in logs

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Load environment and configuration
ENV = os.getenv("APP_ENV", "dev")  # Default to 'dev'
CONFIG_PATH = f"config/{ENV}/config.yaml"

if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(f"⚠️ Configuration file {CONFIG_PATH} not found!")

try:
    with open(CONFIG_PATH, "r") as file:
        config = yaml.safe_load(file)
    LOG_LEVEL = config.get("logging", {}).get("level", "INFO").upper()  # Default to INFO if missing
except Exception as e:
    LOG_LEVEL = "INFO"
    print(f"⚠️ Failed to load logging config: {e}, defaulting to INFO.")

# Remove default Loguru handlers
logger.remove()

# Add Console Logging
logger.add(
    sys.stdout,
    level=LOG_LEVEL,
    enqueue=True,
    backtrace=True,
    diagnose=True
)

# Add Rotating File Logging
logger.add(
    os.path.join(LOG_DIR, "app.log"),
    rotation="10 MB",  # Rotate log when it reaches 10MB
    retention="7 days",  # Keep logs for 7 days
    compression="zip",  # Compress old logs
    level=LOG_LEVEL,
    enqueue=True,
    backtrace=True,
    diagnose=True
)

# ✅ Intercept Flask Logs & Redirect to Loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            request_id = getattr(request, "environ", {}).get("HTTP_X_REQUEST_ID", "N/A")
        except RuntimeError:
            request_id = "N/A"  # Happens if logging outside request context
        logger_opt = logger.bind(request_id=request_id)
        logger_opt.opt(depth=6, exception=record.exc_info).log(record.levelno, record.getMessage())

# Apply logging interception **only if not already set**
if not logging.getLogger().handlers:
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)

# Redirect Flask's default logging (werkzeug, flask) to Loguru **without duplicates**
for _log in ("werkzeug", "flask"):
    _logger = logging.getLogger(_log)
    _logger.handlers.clear()  # Remove default handlers
    _logger.addHandler(InterceptHandler())  # Add Loguru handler
    _logger.propagate = False  # Prevent duplicate logging

logger.info("✅ Logging initialized successfully!")
