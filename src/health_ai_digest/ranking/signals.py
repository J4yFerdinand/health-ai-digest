from datetime import datetime, timezone

from health_ai_digest.models.article import Article

class SignalCalculator:
  @staticmethod
  def recency_score(article: Article) -> float:
    if article.published_at is None:
      return 0.0
    
    now = datetime.now(timezone.utc)

    published_at = article.published_at

    if published_at.tzinfo is None:
      published_at = published_at.replace(tzinfo=timezone.utc)

    days_old = (now - published_at).days

    if days_old <= 30:
      return 1.0
    if days_old <= 90:
      return 0.8
    if days_old <= 180:
      return 0.6
    if days_old <= 365:
      return 0.4
    
    return 0.2