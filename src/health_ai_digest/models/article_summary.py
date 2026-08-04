from pydantic import BaseModel

from .ranked_article import RankedArticle


class ArticleSummary(BaseModel):
    ranked_article: RankedArticle
    summary: str
    key_takeaway: str
