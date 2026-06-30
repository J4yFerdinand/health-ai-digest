from datetime import datetime, timedelta, timezone

from health_ai_digest.models.article import Article
from health_ai_digest.models.enums import SourceType
from health_ai_digest.ranking import SignalCalculator

def create_article(days_old=None):
  published_at = None

  if days_old is not None:
    published_at = datetime.now(timezone.utc) - timedelta(days=days_old)

  return Article(
    title="AI Paper",
    source=SourceType.PUBMED,
    url="https://example.com",
    published_at=published_at,
  )

def test_recency_score_without_date():
  article = create_article()

  score = SignalCalculator.recency_score(article)

  assert score == 0.0

def test_recency_score_recent_article():
  article = create_article(days_old=10)

  score = SignalCalculator.recency_score(article)

  assert score == 1.0

def test_recency_score_old_article():
  article = create_article(days_old=500)

  score = SignalCalculator.recency_score(article)

  assert score == 0.2