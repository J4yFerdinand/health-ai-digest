import pytest
from pydantic import ValidationError
from datetime import datetime

from health_ai_digest.models import ArticleSummary

def test_article_summary_creation(article_summary_factory):
  # An ArticleSummary should be created successfully with valid ranked article and summary data.
  article_summary = article_summary_factory(
    title="AI improves cancer detection",
    score=0.92,
    relevance_score=0.85,
    recency_score=0.95,
    quality_score=0.80,
    summary="Researchers developed an AI model that improved cancer detection accuracy.",
    key_takeaway="AI significantly improves diagnostic perfomance.",
  )

  assert article_summary.summary == (
    "Researchers developed an AI model that improved cancer detection accuracy."
  )
  assert article_summary.key_takeaway == "AI significantly improves diagnostic perfomance."

def test_article_summary_requires_summary(article_summary_factory):
  # Summary is a required field
  with pytest.raises(ValidationError):
    article_summary_factory(summary=None)

def test_article_summary_requires_key_takeaways(article_summary_factory):
  # Key takeaways is a required field
  with pytest.raises(ValidationError):
    article_summary_factory(key_takeaway=None)

def test_article_preserves_ranked_article(article_summary_factory):
  # The wrapped RankedArticle should remain accesible.
  article_summary = article_summary_factory(
    title="Machine Learning for Radiology",
    score=0.88,
    recency_score=1.0,
  )

  assert article_summary.ranked_article.article.title == (
    "Machine Learning for Radiology"
  )
  assert article_summary.ranked_article.overall_score == 0.88
  assert article_summary.ranked_article.recency_score == 1.0