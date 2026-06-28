from datetime import datetime, timezone
from unittest.mock import patch

from health_ai_digest.config.settings import settings
from health_ai_digest.models import Article, SourceType, RankedArticle
from health_ai_digest.ranking.scoring import ScoringEngine

def create_article() -> Article:
  return Article(
    title="AI diagnosis paper",
    url="https://paper1",
    source=SourceType.PUBMED,
    published_at=datetime.now(timezone.utc),
    doi="10.1000/test"
  )

def test_score_returns_ranked_article():
  article = create_article()

  ranked = ScoringEngine.score(article)

  assert isinstance(ranked, RankedArticle)
  assert ranked.article == article

@patch("health_ai_digest.ranking.scoring.SignalCalculator.recency_score")
def test_score_computes_weighted_sum(mock_recency):
  article = create_article()

  mock_recency.return_value = 0.6

  ranked = ScoringEngine.score(article)

  expected_score = (
    0.0 * settings.ranking_relevance_weight  # relevance
    + 0.6 * settings.ranking_recency_weight   # recency
    + 0.0 * settings.ranking_quality_weight     # quality
  )

  assert ranked.score == expected_score
  assert ranked.recency_score == 0.6

@patch("health_ai_digest.ranking.scoring.SignalCalculator.recency_score")
def test_score_preserves_individual_signals(mock_recency):
  article = create_article()

  mock_recency.return_value = 1.0

  ranked = ScoringEngine.score(article)

  assert ranked.relevance_score == 0.0
  assert ranked.recency_score == 1.0
  assert ranked.quality_score == 0.0
