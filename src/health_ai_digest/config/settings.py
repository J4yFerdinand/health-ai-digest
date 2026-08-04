from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # PubMed
    pubmed_search_url: str = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    )
    pubmed_fetch_url: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    pubmed_timeout: int = 15
    pubmed_default_limit: int = 10

    # Ranking
    ranking_relevance_weight: float = 0.5
    ranking_recency_weight: float = 0.3
    ranking_quality_weight: float = 0.2

    ranking_recency_threshold_fresh: int = 30
    ranking_recency_threshold_recent: int = 90
    ranking_recency_threshold_stale: int = 180
    ranking_recency_threshold_old: int = 365

    # LLM
    llm_provider: str = "groq"
    llm_timeout: int = 60
    llm_max_retries: int = 3

    # Groq
    groq_model: str = "llama-3.3-70b-versatile"
    groq_temperature: float = 0.2
    groq_max_tokens: int = 700

    # Digest
    digest_max_articles: int = 10
    digest_summary_max_chars: int = 1200
    digest_key_takeaway_max_chars: int = 300

    # # Export
    # digest_output_dir: str = "outputs"
    # digest_filename_prefix: str = "health_digest"

    # # Project
    # project_name: str = "health-ai-digest"
    # project_version: str = "0.1.0"


settings = Settings()
