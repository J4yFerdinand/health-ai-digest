from datetime import datetime
from pydantic import BaseModel, Field

from health_ai_digest.models.enums import SourceType

class Article(BaseModel):
  title: str = Field(..., min_length=3)
  source: SourceType
  url: str

  abstract: str | None = None
  authors: list[str] = Field(default_factory=list)
  published_at: datetime | None = None
  keywords: list[str] = Field(default_factory=list)
  doi: str | None = None