from datetime import datetime

import pytest
from pydantic import ValidationError

from health_ai_digest.models import Digest

def test_digest_creation(article_summary_factory):
  # A Digest should be created successfully.

  summary = article_summary_factory(
    title="AI detects penumonia"
  )

  digest = Digest(
    generated_at=datetime(2026, 7, 3),
    articles=[summary],
  )

  assert digest.generated_at == datetime(2026, 7, 3)
  assert len(digest.articles) == 1
  assert digest.articles[0] == summary

def test_digest_requires_generated_at(article_summary_factory):
  # generated_at is required.

  summary = article_summary_factory()

  with pytest.raises(ValidationError):
    Digest(
      articles=[summary],
    )

def test_digest_requires_articles():
  # articles is required.

  with pytest.raises(ValidationError):
    Digest(
      generated_at=datetime.now(),
    )

def test_digest_preserves_article_summaries(article_summary_factory):
  # Digest should preserve wrapped ArticleSummary instances.

  summary = article_summary_factory(
    title="Deep Learning for Cardiology"
  )

  digest = Digest(
    generated_at=datetime.now(),
    articles=[summary],
  )

  assert digest.articles[0].ranked_article.article.title == "Deep Learning for Cardiology"