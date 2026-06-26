from health_ai_digest.ingestion.pubmed import PubMedClient
from health_ai_digest.aggregation.aggregator import AggregationService

def main():
  pubmed = PubMedClient()

  aggregator = AggregationService(
    clients=[pubmed]
  )

  articles = aggregator.aggregate(
    query="artificial intelligence diagnosis",
    limit=2,
  )

  duplicated_articles = articles + articles
  print("Before:", len(duplicated_articles))

  deduplicated = aggregator.deduplicator.deduplicate(duplicated_articles)
  print("After:", len(deduplicated))

if __name__ == "__main__":
  main()