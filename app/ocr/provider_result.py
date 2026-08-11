"""Provider-neutral result envelope with safe serialization."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
import re
from typing import Any


_SENSITIVE_FRAGMENTS = (
    "api_key", "apikey", "secret", "password", "credential", "token",
    "authorization", "traceback", "stack_trace",
)


def _safe_value(key: str, value: Any) -> Any:
    if any(fragment in key.casefold() for fragment in _SENSITIVE_FRAGMENTS):
        return "[REDACTED]"
    if isinstance(value, BaseException):
        return type(value).__name__
    if isinstance(value, Path):
        return value.name
    if isinstance(value, dict):
        return {str(k): _safe_value(str(k), v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_safe_value(key, item) for item in value]
    if isinstance(value, str) and "path" in key.casefold():
        return Path(value).name
    return value


@dataclass
class ProviderResult:
    provider: str
    model: str
    image_identifier: str
    extracted_text: str = ""
    page_count: int = 1
    latency_ms: float | None = None
    success: bool = True
    error_type: str | None = None
    estimated_cost_usd: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.page_count < 0:
            raise ValueError("page_count cannot be negative")
        if self.latency_ms is not None and self.latency_ms < 0:
            raise ValueError("latency_ms cannot be negative")
        if self.estimated_cost_usd is not None and self.estimated_cost_usd < 0:
            raise ValueError("estimated_cost_usd cannot be negative")
        # Store only the image's identifier, never a caller's full local path.
        self.image_identifier = Path(self.image_identifier).name
        if isinstance(self.error_type, BaseException):
            self.error_type = type(self.error_type).__name__
        elif self.error_type is not None:
            # An error category is useful; messages and tracebacks are not.
            match = re.search(r"[A-Za-z_][A-Za-z0-9_]*(?:Error|Exception|Timeout)?", self.error_type)
            self.error_type = match.group(0) if match else "ProviderError"
        self.metadata = _safe_value("metadata", self.metadata)

    def to_dict(self) -> dict[str, Any]:
        return _safe_value("result", asdict(self))

    def model_dump(self) -> dict[str, Any]:
        """Pydantic-compatible convenience method."""
        return self.to_dict()
