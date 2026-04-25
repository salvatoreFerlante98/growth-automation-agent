"""Log and error code registry.

Every code used in AppLogger or AppError must be declared here.
Format: <PREFIX>-<NNN>
  INF — informational
  WRN — warning (recoverable, execution continues)
  ERR — error (operation failed)
  DBG — debug / tracing
"""

from enum import StrEnum


class LogCode(StrEnum):
    # INFO
    INF_GENERIC = "INF-000"
    INF_CSV_LOADED = "INF-001"
    INF_LEAD_CREATED = "INF-002"

    # WARNING
    WRN_GENERIC = "WRN-000"
    WRN_CSV_ROW_SKIPPED = "WRN-001"

    # ERROR
    ERR_GENERIC = "ERR-000"
    ERR_FILE_NOT_FOUND = "ERR-001"
    ERR_CSV_PARSE = "ERR-002"
    ERR_LEAD_VALIDATION = "ERR-003"
    ERR_DB_WRITE = "ERR-004"

    # DEBUG
    DBG_GENERIC = "DBG-000"
