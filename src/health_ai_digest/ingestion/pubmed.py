import requests

from health_ai_digest.ingestion.base import BaseIngestionClient
from health_ai_digest.models.article import Article

class PubMedClient(BaseIngestionClient):
  SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

  def fetch(self, query: str, limit: int = 10) -> list[Article]:
    pmids = self._search(query, limit)
    print(pmids)

    return []
  
  def _search(self, query: str, limit: int) -> list[str]:
    params = {
      "db": "pubmed",
      "term": query,
      "retmax": limit,
      "retmode": "json",
    }

    response = requests.get(self.SEARCH_URL, params=params)
    response.raise_for_status()

    data = response.json()

    return data["esearchresult"]["idlist"]