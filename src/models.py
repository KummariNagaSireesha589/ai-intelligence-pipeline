from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, HttpUrl, Field

RecordType = Literal["STARTUP", "PRODUCT", "RESEARCH_PAPER", "JOB", "NEWS"]

class Source(BaseModel):
    name: str
    url: HttpUrl

class EntityRecord(BaseModel):
    schemaVersion: str = "1.0"
    recordType: RecordType
    source: Source
    content: dict[str, Any]
    collectedAt: datetime = Field(default_factory=datetime.utcnow)

class MappingLog(BaseModel):
    raw_name: str
    canonical_name: str
    method: str
    confidence: float
