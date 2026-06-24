from health_ai_digest.models.article import Article
from health_ai_digest.ingestion.base import BaseIngestionClient

class AggregationService:
  def __init__(self, clients: list[BaseIngestionClient]):
    self.clients = clients

  def aggregate(self, query: str, limit: int = 5) -> list[Article]:
    all_articles: list[Article] = []

    for client in self.clients:
      articles = client.fetch(query=query, limit=limit)
      all_articles.extend(articles)

    return all_articles