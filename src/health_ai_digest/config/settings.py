from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
  # PubMed
  pubmed_search_url: str = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
  )
  pubmed_fetch_url: str = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
  )
  pubmed_timeout: int = 15
  pubmed_default_limit: int = 10

  # Ranking
  ranking_relevance_weight: float = 0.5
  ranking_recency_weight: float = 0.3
  ranking_quality_weight: float = 0.2

settings = Settings()