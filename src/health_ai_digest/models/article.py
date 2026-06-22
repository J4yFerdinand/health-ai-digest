from datetime import datetime
from pydantic import BaseModel, Field

from health_ai_digest.models.enums import SourceType

class Article(BaseModel):
  title: str = Field(..., min_length=3)
  source: SourceType
  url: str

  abstract: str | None = None
  authors: list[str] = []
  published_at: datetime | None = None
  keywords: list[str] = []
  doi: str | None = None