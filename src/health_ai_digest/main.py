from health_ai_digest.ingestion.pubmed import PubMedClient

def main():
  client = PubMedClient()

  articles = client.fetch(
    query="artificial intelligence diagnosis",
    limit=3,
  )

  for i, article in enumerate(articles, start=1):
    print("=" * 100)
    print(f"ARTICLE #{i}")
    print("=" * 100)

    print("TITLE:", article.title)
    print("SOURCE:", article.source)
    print("URL:", article.url)
    print("AUTHORS:", article.authors)
    print("PUBLISHED:", article.published_at)
    print("DOI:", article.doi)

    if article.abstract:
      preview = article.abstract[:500]
      print("ABSTRACT:", preview)

    if len(article.abstract) > 500:
      print("... [TRUNCATED]")
    else:
      print("ABSTRACT: None")

    print()


if __name__ == "__main__":
  main()