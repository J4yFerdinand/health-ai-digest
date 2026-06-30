import pytest
from pydantic import ValidationError

from datetime import datetime

from health_ai_digest.models.article import Article
from health_ai_digest.models.enums import SourceType
from health_ai_digest.models.ranked_article import RankedArticle

def test_ranked_article_creation():
  article = Article(
    title="AI in Healthcare",
    source=SourceType.PUBMED,
    url="https://example.com",
    published_at=datetime.now(),
  )

  ranked = RankedArticle(
    article=article,
    score=0.85,
  )

  assert ranked.article == article
  assert ranked.score == 0.85

def test_ranked_article_default_signal_scores():
  article = Article(
    title="AI in Healthcare",
    source=SourceType.PUBMED,
    url="https://example.com",
  )

  ranked = RankedArticle(
    article=article,
    score=0.7,
  )

  assert ranked.relevance_score == 0.0
  assert ranked.recency_score == 0.0
  assert ranked.quality_score == 0.0

def test_ranked_article_rejects_negative_score():
  article = Article(
    title="AI in Healthcare",
    source=SourceType.PUBMED,
    url="https://example.com",
  )

  with pytest.raises(ValidationError):
    RankedArticle(
      article=article,
      score=-1.0
    )