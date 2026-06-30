from health_ai_digest.config.settings import settings
from health_ai_digest.models import Article, RankedArticle
from health_ai_digest.ranking.signals import SignalCalculator

class ScoringEngine:
  @classmethod
  def score(cls, article: Article) -> RankedArticle:
    # Compute weighted ranking score for a single article.
    relevance_score = 0.0
    recency_score = SignalCalculator.recency_score(article)
    quality_score = 0.0

    final_score = (
      relevance_score * settings.ranking_relevance_weight
      + recency_score * settings.ranking_recency_weight
      + quality_score * settings.ranking_quality_weight
    )

    return RankedArticle(
      article=article,
      score=final_score,
      relevance_score=relevance_score,
      recency_score=recency_score,
      quality_score=quality_score
    )
  