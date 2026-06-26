from health_ai_digest.aggregation.aggregator import AggregationService
from health_ai_digest.models.article import Article

class FakeIngestionClient:
  def __init__(self, articles: list[Article]):
    self.articles = articles

  def fetch(self, query: str, limit: int = 5) -> list[Article]:
    return self.articles
  
def test_aggregator_merges_articles_from_multiple_clients(article_factory):
  client_1 = FakeIngestionClient([
    article_factory("Paper 1", "https://paper1", "10.1"),
    article_factory("Paper 2", "https://paper2", "10.2"),
    ])

  client_2 = FakeIngestionClient([
    article_factory("Paper 3", "https://paper3", "10.3"),
    article_factory("Paper 4", "https://paper4", "10.4"),
    article_factory("Paper 5", "https://paper5", "10.5"),
  ])

  aggregator = AggregationService([client_1, client_2])

  result = aggregator.aggregate("ai")

  assert len(result) == 5

def test_aggregator_removes_duplicates(article_factory):
  duplicate_1 = article_factory(
    "AI Cancer Detection",
    "https://paper1",
    "10.1000/shared"
  )

  duplicate_2 = article_factory(
    "AI Cancer Detection",
    "https://paper2",
    "10.1000/shared"
  )

  client_1 = FakeIngestionClient([duplicate_1])
  client_2 = FakeIngestionClient([duplicate_2])

  aggregator = AggregationService([client_1, client_2])

  result = aggregator.aggregate("ai")

  assert len(result) == 1
  assert result[0].doi == "10.1000/shared"