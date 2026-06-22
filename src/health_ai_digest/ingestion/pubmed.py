import requests

from health_ai_digest.ingestion.base import BaseIngestionClient
from health_ai_digest.models.article import Article

class PubMedClient(BaseIngestionClient):
  SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
  FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

  def fetch(self, query: str, limit: int = 10) -> list[Article]:
    # Search PubMed and fetch full metadata for the resulting articles.
    pmids = self._search(query, limit)
    xml_data = self._fetch_details(pmids)

    # Temporal: Manual Inspection of XML
    print(xml_data[:1000])

    return []
  
  def _search(self, query: str, limit: int) -> list[str]:
    # Search PubMed and return a list of PMIDs.
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
  
  def _fetch_details(self, pmids: list[str]) -> str:
    """
    Fetch article metadata from PubMed using PMIDs.
    Returns raw XML response.
    """
    if not pmids:
      return ""
    
    params = {
      "db": "pubmed",
      "id": ",".join(pmids),
      "retmode": "xml"
    }

    response = requests.get(self.FETCH_URL, params=params)
    response.raise_for_status()

    return response.text