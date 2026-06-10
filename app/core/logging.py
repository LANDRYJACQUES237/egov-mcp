import logging
import json
import uuid
from datetime import datetime, timezone
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar("request_id", default="")


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "request_id": request_id_var.get(""),
            "message": record.getMessage(),
            "module": record.module,
        }
        return json.dumps(log_entry, ensure_ascii=False)


def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logging.basicConfig(level=getattr(logging, level), handlers=[handler])


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def new_request_id() -> str:
    rid = str(uuid.uuid4())[:8]
    request_id_var.set(rid)
    return rid
