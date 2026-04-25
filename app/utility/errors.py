"""Custom application exception.

Carries a LogCode so callers can catch and branch on specific error types
without relying on message string matching.

Usage:
    raise AppError(LogCode.ERR_FILE_NOT_FOUND, f"No such file: {path}")

    try:
        ...
    except AppError as exc:
        if exc.code == LogCode.ERR_LEAD_VALIDATION:
            ...  # handle validation failures specifically
        raise
"""

from app.utility.codes import LogCode


class AppError(Exception):
    def __init__(self, code: LogCode, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"[{code}] {detail}" if detail else f"[{code}]")
