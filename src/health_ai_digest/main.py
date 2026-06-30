from health_ai_digest.ingestion.pubmed import PubMedClient

def main():
  client = PubMedClient()
  articles = client.fetch("artificial intelligence diagnosis", limit=3)

  # print("Articles:", articles)
  # print("Count:", len(articles))

  for article in articles:
    print("=" * 80)
    print(f"TITLE: {article.title}")
    print(f"SOURCE: {article.source}")
    print(f"URL: {article.url}")

if __name__ == "__main__":
  main()