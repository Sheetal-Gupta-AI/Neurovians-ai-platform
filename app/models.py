"""The minimal LLM registry contract used by both UI and API."""

from enum import Enum

from pydantic import BaseModel, Field


class ModelStatus(str, Enum):
    AVAILABLE = "available"
    DISABLED = "disabled"
    NOT_CONFIGURED = "not_configured"
    VALIDITY        = "valid"


class RegisteredLLM(BaseModel):
    model_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    status: ModelStatus = ModelStatus.AVAILABLE
    endpoint_or_path: str | None = None
