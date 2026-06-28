from health_ai_digest.models import Article, RankedArticle
from health_ai_digest.ranking.scoring import ScoringEngine

class Ranker:
  # Rank a collection of articles using the scoring engine.
  @classmethod
  def rank(cls, articles: list[Article]) -> list[RankedArticle]:
    """
    Score and rank articles in descending order.

    Args:
      articles: List of articles to rank.

    Returns:
      Ranked articles sorted by descending score.
    """
    if not articles:
      return []
    
    ranked_articles = [
      ScoringEngine.score(article)
      for article in articles
    ]

    ranked_articles.sort(
      key=lambda ranked_article: ranked_article.score,
      reverse=True
    )

    return ranked_articles