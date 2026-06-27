from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
  pubmed_search_url: str = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
  )
  pubmed_fetch_url: str = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
  )
  pubmed_timeout: int = 15
  pubmed_default_limit: int = 10

settings = Settings()