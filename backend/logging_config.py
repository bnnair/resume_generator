# In this file, you can set the configurations of the app.

# logging_config.py
from loguru import logger
import os
import sys

# Remove default logger
logger.remove()

log_folder = 'log'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file = os.path.join(log_folder, 'app_log.log')

# Configure the logger
logger.add(
    log_file,  # Log file name
    # level="INFO",  # Minimum log level
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",  # Log format
    rotation="10 MB",  # Rotate log files when they reach 10 MB
    retention="30 days",  # Retain logs for 30 days
    compression="zip",  # Compress rotated logs
    enqueue=True,  # Thread-safe logging
)
MINIMUM_LOG_LEVEL = "DEBUG"
if MINIMUM_LOG_LEVEL in ["DEBUG", "TRACE", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    logger.remove()
    logger.add(sys.stderr, level=MINIMUM_LOG_LEVEL)
    # # Add a sink to log to a file
    # logger.add(log_file, rotation="5 MB", format="{time} {level} {message}")
else:
    logger.warning(
        f"Invalid log level: {MINIMUM_LOG_LEVEL}. Defaulting to DEBUG.")
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")

# Optional: Environment-specific logging
if os.getenv("ENVIRONMENT") == "production":
    logger.add("errors.log", level="ERROR")

# Export the configured logger
logger.info("Logging configuration loaded")


"""
MINIMUM_LOG_LEVEL can only be one of the followings:
    - "DEBUG"
    - "INFO"
    - "WARNING"
    - "ERROR"
    - "CRITICAL"
"""
