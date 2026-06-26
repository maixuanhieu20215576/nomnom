from typing import Literal

from fastapi import APIRouter, HTTPException

from app.core.logging_config import ALL_LOG_FILE, ERROR_LOG_FILE, SCHEDULER_LOG_FILE

router = APIRouter(prefix="/logs", tags=["logs"])

LOG_FILES = {
    "scheduler": SCHEDULER_LOG_FILE,
    "error": ERROR_LOG_FILE,
    "all": ALL_LOG_FILE,
}


@router.get("/{log_type}")
async def read_log_route(log_type: Literal["scheduler", "error", "all"], lines: int = 200):
    file_path = LOG_FILES[log_type]

    try:
        with open(file_path, "r") as f:
            all_lines = f.readlines()
    except FileNotFoundError:
        return {"lines": []}

    return {"lines": [line.rstrip("\n") for line in all_lines[-lines:]]}
