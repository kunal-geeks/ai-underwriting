import logging
import sys
import json
import os
from logging.handlers import RotatingFileHandler

class JSONLogFormatter(logging.Formatter):
    def format(self, record):
        log_message = super().format(record)
        log_data = {
            'timestamp': self.formatTime(record, self.datefmt),
            'name': record.name,
            'level': record.levelname,
            'message': log_message,
            'thread': record.threadName,
            'file': record.pathname,
            'line': record.lineno,
        }
        return json.dumps(log_data)

class LogFormatter(logging.Formatter):
    COLOR_CODES = {
        logging.CRITICAL: "\033[1;35m",  # bright/bold magenta
        logging.ERROR: "\033[1;31m",  # bright/bold red
        logging.WARNING: "\033[1;33m",  # bright/bold yellow
        logging.INFO: "\033[0;37m",  # white / light gray
        logging.DEBUG: "\033[1;30m"  # bright/bold dark gray
    }
    RESET_CODE = "\033[0m"

    def format(self, record):
        log_message = super().format(record)
        if record.levelno in self.COLOR_CODES:
            color_on = self.COLOR_CODES[record.levelno]
            color_off = self.RESET_CODE
            return f"{color_on}{log_message}{color_off}"
        return log_message

def get_logger(console_log_output="stdout", console_log_level="INFO",
               logfile_file="logs/automation.log", logfile_log_level="DEBUG",
               max_log_size=10 * 1024 * 1024, backup_count=5, json_log=False):
    """
    Set up a shared logger across modules with console and rotating file support.
    Automatically creates the logs folder if it does not exist.
    """
    logger_name = sys._getframe(1).f_globals["__name__"]
    logger = logging.getLogger(logger_name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    output_stream = sys.stdout if console_log_output.lower() == "stdout" else sys.stderr
    console_handler = logging.StreamHandler(output_stream)

    try:
        console_handler.setLevel(console_log_level.upper())
    except ValueError:
        print(f"Invalid console log level: {console_log_level}")
        return None

    # Use JSON formatter if json_log is True, otherwise use the regular formatter
    console_formatter = JSONLogFormatter() if json_log else LogFormatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Ensure the logs folder exists
    log_dir = os.path.dirname(logfile_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    try:
        logfile_handler = RotatingFileHandler(logfile_file, maxBytes=max_log_size, backupCount=backup_count)
        logfile_handler.setLevel(logfile_log_level.upper())

        logfile_formatter = JSONLogFormatter() if json_log else logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        logfile_handler.setFormatter(logfile_formatter)
        logger.addHandler(logfile_handler)
    except Exception as e:
        print(f"Failed to set up log file: {e}")
        return None

    return logger
