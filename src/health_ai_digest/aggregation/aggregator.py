from health_ai_digest.models.article import Article
from health_ai_digest.ingestion.base import BaseIngestionClient
from health_ai_digest.aggregation.deduplicator import Deduplicator

class AggregationService:
  def __init__(self, clients: list[BaseIngestionClient]):
    self.clients = clients
    self.deduplicator = Deduplicator()

  def aggregate(self, query: str, limit: int = 5) -> list[Article]:
    all_articles: list[Article] = []

    for client in self.clients:
      articles = client.fetch(query=query, limit=limit)
      all_articles.extend(articles)

    deduplicated_articles = self.deduplicator.deduplicate(all_articles)

    return deduplicated_articles