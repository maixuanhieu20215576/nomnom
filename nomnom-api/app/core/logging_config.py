import logging
import logging.handlers
import os

LOG_DIR = "logs"

SCHEDULER_LOG_FILE = os.path.join(LOG_DIR, "scheduler.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")
ALL_LOG_FILE = os.path.join(LOG_DIR, "all.log")

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"


def _make_rotating_handler(filename: str, backup_days: int, level: int) -> logging.Handler:
    handler = logging.handlers.TimedRotatingFileHandler(
        filename, when="midnight", backupCount=backup_days, utc=True
    )
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return handler


def setup_logging() -> None:
    os.makedirs(LOG_DIR, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # all.log: every log record, short retention since it's the highest volume
    root_logger.addHandler(_make_rotating_handler(ALL_LOG_FILE, backup_days=3, level=logging.INFO))

    # error.log: only errors, kept the longest for incident investigation
    root_logger.addHandler(_make_rotating_handler(ERROR_LOG_FILE, backup_days=30, level=logging.ERROR))

    # scheduler.log: only logs from app.core.scheduler (job runs)
    scheduler_handler = _make_rotating_handler(SCHEDULER_LOG_FILE, backup_days=7, level=logging.INFO)
    logging.getLogger("app.core.scheduler").addHandler(scheduler_handler)
