from datetime import datetime

from pydantic import BaseModel, Field

from health_ai_digest.models import ArticleSummary


class Digest(BaseModel):
    # Represents a complete AI-generated digest.

    generated_at: datetime = Field(
        description="Timestamp when the digest was generated."
    )
    articles: list[ArticleSummary] = Field(
        description="Summarized articles included in the digest."
    )
