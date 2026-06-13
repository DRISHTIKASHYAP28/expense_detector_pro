"""
logging_config.py
-----------------
Centralised logging configuration for the entire application.

Uses Python's standard `logging` module — no third-party dependency needed.
Configures two handlers:
  1. StreamHandler  → writes to stdout (captured by Docker/systemd/Heroku logs)
  2. FileHandler    → writes to logs/app.log for local inspection

Format includes timestamp, log level, module name, and the message — making it
straightforward to trace which layer (route/service/repository) raised an issue.

Usage:
    from logging_config import setup_logging
    setup_logging(log_level="DEBUG")
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure root logger with console and rotating file handlers.

    Args:
        log_level: One of DEBUG, INFO, WARNING, ERROR, CRITICAL.
                   Typically pulled from config.LOG_LEVEL.
    """
    # Ensure the logs directory exists
    os.makedirs("logs", exist_ok=True)

    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Log format: 2024-01-15 12:30:00,123 [INFO] services.auth_service: User registered.
    log_format = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── Handler 1: stdout console ─────────────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(log_format)

    # ── Handler 2: rotating file (max 5 MB × 3 backup files) ─────────────────
    file_handler = RotatingFileHandler(
        filename="logs/app.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(log_format)

    # Configure the root logger — all child loggers (per module) inherit this.
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Avoid adding duplicate handlers if setup_logging is called more than once
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)
