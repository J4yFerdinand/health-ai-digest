from pydantic import BaseModel

from health_ai_digest.models import RankedArticle

class ArticleSummary(BaseModel):
  ranked_article: RankedArticle
  summary: str
  key_takeaway: str