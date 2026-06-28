from datetime import datetime, timezone
from unittest.mock import patch

from health_ai_digest.models import (
  Article,
  RankedArticle,
  SourceType,
)
from health_ai_digest.ranking.ranker import Ranker

def create_article(title: str) -> Article:
  return Article(
    title=title,
    url=f"https://{title}.com",
    source=SourceType.PUBMED,
    published_at=datetime.now(timezone.utc),
    doi=f"10.1000/{title}"
  )

def test_rank_returns_empty_list_when_no_articles():
  result = Ranker.rank([])

  assert result == []

@patch("health_ai_digest.ranking.ranker.ScoringEngine.score")
def test_rank_returns_ranked_articles(mock_score):
  article1 = create_article("paper1")
  article2 = create_article("paper2")

  mock_score.side_effect = [
    RankedArticle(article=article1, score=0.5),
    RankedArticle(article=article2, score=0.8),
  ]

  result = Ranker.rank([article1, article2])

  assert len(result) == 2
  assert all(isinstance(item, RankedArticle) for item in result)

@patch("health_ai_digest.ranking.ranker.ScoringEngine.score")
def test_rank_sorts_articles_by_score_desc(mock_score):
  article1 = create_article("paper1")
  article2 = create_article("paper2")
  article3 = create_article("paper3")

  ranked1 = RankedArticle(article=article1, score=0.4)
  ranked2 = RankedArticle(article=article2, score=0.95)
  ranked3 = RankedArticle(article=article3, score=0.7)

  mock_score.side_effect = [ranked1, ranked2, ranked3]

  result = Ranker.rank([article1, article2, article3])

  assert result[0].score == 0.95
  assert result[1].score == 0.7
  assert result[2].score == 0.4