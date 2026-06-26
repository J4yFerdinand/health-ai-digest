from health_ai_digest.models.article import Article

class Deduplicator:
  def deduplicate(self, articles: list[Article]) -> list[Article]:
    unique_articles: list[Article] = []

    seen_dois: set[str] = set()
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()

    for article in articles:
      if article.doi and article.doi in seen_dois:
        continue

      if article.url in seen_urls:
        continue

      normalized_title = article.title.lower().strip()
      if normalized_title in seen_titles:
        continue

      unique_articles.append(article)

      if article.doi:
        seen_dois.add(article.doi)

      seen_urls.add(article.url)
      seen_titles.add(normalized_title)

    return unique_articles