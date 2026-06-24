from health_ai_digest.ingestion.pubmed import PubMedClient
from health_ai_digest.aggregation.aggregator import AggregationService

def main():
  pubmed = PubMedClient()

  aggregator = AggregationService(
    clients=[pubmed]
  )

  articles = aggregator.aggregate(
    query="artificial intelligence diagnosis",
    limit=3,
  )

  for article in articles:
    print("=" * 80)
    print(article.title)
    print(article.source)
    print(article.doi)

if __name__ == "__main__":
  main()