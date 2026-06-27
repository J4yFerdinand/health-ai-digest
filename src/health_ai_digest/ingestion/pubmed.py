import requests
import xml.etree.ElementTree as ET

from datetime import datetime

from health_ai_digest.config.settings import settings
from health_ai_digest.ingestion.base import BaseIngestionClient
from health_ai_digest.models.article import Article
from health_ai_digest.models.enums import SourceType

class PubMedClient(BaseIngestionClient):

  def fetch(self, query: str, limit: int | None = None) -> list[Article]:
    # Search PubMed and fetch full metadata for the resulting articles.
    limit = limit or settings.pubmed_default_limit

    pmids = self._search(query, limit)

    xml_data = self._fetch_details(pmids)

    articles = self._parse_articles(xml_data)

    return articles
  
  def _search(self, query: str, limit: int) -> list[str]:
    # Search PubMed and return a list of PMIDs.
    params = {
      "db": "pubmed",
      "term": query,
      "retmax": limit,
      "retmode": "json",
    }

    response = requests.get(
      settings.pubmed_search_url,
      params=params,
      timeout=settings.pubmed_timeout,
    )
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

    response = requests.get(
      settings.pubmed_fetch_url,
      params=params,
      timeout=settings.pubmed_timeout,
    )
    response.raise_for_status()
    
    return response.text
  
  def _parse_articles(self, xml_data: str) -> list[Article]:
    if not xml_data:
      return []
    
    root = ET.fromstring(xml_data)
    articles = []

    for pubmed_article in root.findall(".//PubmedArticle"):
      article = self._parse_article(pubmed_article)
      articles.append(article)

    return articles
  
  def _parse_article(self, pubmed_article: ET.Element) -> Article:
    # Parse a single PubMed article.
    pmid = pubmed_article.findtext(".//PMID", default="")
    title = pubmed_article.findtext(".//ArticleTitle", default="Untitled")

    url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

    authors = self._extract_authors(pubmed_article)
    published_at = self._extract_published_at(pubmed_article)
    abstract = self._extract_abstract(pubmed_article)
    doi = self._extract_doi(pubmed_article)

    return Article(
      title=title,
      source=SourceType.PUBMED,
      url=url,
      authors=authors,
      published_at=published_at,
      abstract=abstract,
      doi=doi,
    )

  def _extract_authors(self, pubmed_article: ET.Element) -> list[str]:
    # Extract author names from PubMed article XML
    authors = []

    for author in pubmed_article.findall(".//Author"):
      fore_name = author.findtext("ForeName")
      last_name = author.findtext("LastName")
      collective_name = author.findtext("CollectiveName")

      if fore_name and last_name:
        authors.append(f"{fore_name} {last_name}")
      elif last_name:
        authors.append(last_name)
      elif collective_name:
        authors.append(collective_name)

    return authors

  def _extract_published_at(
    self,
    pubmed_article: ET.Element,
  ) -> datetime | None:
    # Extract publication date from PubMed article XML.
    pub_date = pubmed_article.find(".//PubDate")

    if pub_date is None:
      return None

    year = pub_date.findtext("Year")
    month = pub_date.findtext("Month", "1")
    day = pub_date.findtext("Day", "1")

    if not year:
      return None

    month_map = {
      "Jan": 1,
      "Feb": 2,
      "Mar": 3,
      "Apr": 4,
      "May": 5,
      "Jun": 6,
      "Jul": 7,
      "Aug": 8,
      "Sep": 9,
      "Oct": 10,
      "Nov": 11,
      "Dec": 12,
    }

    if month.isdigit():
      month_value = int(month)
    else:
      month_value = month_map.get(month, 1)

    try:
      return datetime(int(year), month_value, int(day))
    except ValueError:
      return None
    
  def _extract_abstract(self, pubmed_article: ET.Element) -> str | None:
    # Extract abstract from PubMed XML. Supports both single and multi-section abstracts.
    abstract_nodes = pubmed_article.findall(".//AbstractText")

    if not abstract_nodes:
      return None
    
    sections = []

    for node in abstract_nodes:
      text = "".join(node.itertext()).strip()

      if not text:
        continue

      label = node.attrib.get("Label")

      if label:
        sections.append(f"{label}: {text}")
      else:
        sections.append(text)

    if not sections:
      return None
    
    return "\n\n".join(sections)
  
  def _extract_doi(self, pubmed_article: ET.Element) -> str | None:
    # Extract Doi from PubMed XML
    for article_id in pubmed_article.findall(".//ArticleId"):
      if article_id.attrib.get("IdType") == "doi":
        if article_id.text:
          return article_id.text.strip()
        
    for elocation in pubmed_article.findall(".//ElocationID"):
      if elocation.attrib.get("EIdType") == "doi":
        if elocation.text:
          return elocation.text.strip()
        
    return None