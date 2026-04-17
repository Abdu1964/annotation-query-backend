import os
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
import axiom_py
from axiom_py.logging import AxiomHandler
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from dotenv import load_dotenv

load_dotenv()

def init_logging():
    # Create logs directory for file logging
    logs_dir = Path("/app/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # --- Sentry ---
    DSN = os.getenv("SENTRY_DSN")
    sentry_logging = LoggingIntegration(
        level=logging.INFO,        # Capture >= INFO as breadcrumbs
        event_level=logging.ERROR  # Send ERROR and above as events
    )

    sentry_sdk.init(
        dsn=DSN,
        integrations=[sentry_logging],
        send_default_pii=True,
        attach_stacktrace=True
    )

    # --- Create formatter first ---
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # --- Console handler ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # --- Axiom ---
    client = axiom_py.Client()
    dataset_name = os.getenv("AXIOM_DATASET", "application-logs")  # configurable
    axiom_handler = AxiomHandler(client, dataset_name)

    # --- File Handler for Application Logs ---
    file_handler = None
    app_log_file = logs_dir / "application.log"
    try:
        file_handler = RotatingFileHandler(
            app_log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
    except Exception:
        # Keep app startup alive if file handler cannot be initialized.
        logging.getLogger().exception("Failed to initialize application file handler at %s", app_log_file)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Add handlers
    root_logger.addHandler(axiom_handler)

    # Optional: also log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    # Add ALL handlers  
    root_logger.addHandler(axiom_handler)
    if file_handler is not None:
        root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # --- Performance Logs ---
    PERF_LOGS_DATASET = os.getenv("AXIOM_PERFORMANCE_LOGS", "performance-metrics")
    perf_handler = AxiomHandler(client, PERF_LOGS_DATASET)

    # --- File Handler for Performance Logs ---
    perf_file_handler = None
    perf_log_file = logs_dir / "performance.log"
    try:
        perf_file_handler = RotatingFileHandler(
            perf_log_file,
            maxBytes=10*1024*1024,
            backupCount=5,
            encoding='utf-8'
        )
        perf_file_handler.setLevel(logging.INFO)
        perf_file_handler.setFormatter(formatter)
    except Exception:
        logging.getLogger().exception("Failed to initialize performance file handler at %s", perf_log_file)
    
    # --- Performance logger ---
    perf_logger = logging.getLogger("performance")
    perf_logger.setLevel(logging.INFO)
    perf_logger.addHandler(perf_handler)
    if perf_file_handler is not None:
        perf_logger.addHandler(perf_file_handler)
    perf_logger.addHandler(console_handler)
    
    return perf_logger