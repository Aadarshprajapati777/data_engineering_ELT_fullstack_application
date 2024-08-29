# app/core/logging.py
import logging
import json_log_formatter

formatter = json_log_formatter.JSONFormatter()

logger = logging.getLogger("data_engineering")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
