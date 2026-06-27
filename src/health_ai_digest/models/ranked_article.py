from pydantic import BaseModel, Field

from health_ai_digest.models.article import Article

class RankedArticle(BaseModel):
  article: Article
  score: float = Field(..., ge=0.0)

  relevance_score: float = Field(default=0.0, ge=0.0) 
  recency_score: float = Field(default=0.0, ge=0.0) 
  quality_score: float = Field(default=0.0, ge=0.0)
  