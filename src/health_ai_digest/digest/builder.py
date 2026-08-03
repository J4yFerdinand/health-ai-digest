from health_ai_digest.models import RankedArticle

class PromptBuilder:
  # Build prompts for AI summarization.

  def build_system_prompt(self) -> str:
    # Return the system prompt.

    return """
You are an expert medical research analyst specialized in Artificial Intelligence applied to Healthcare.

Your task is to summarize peer-reviewed healthcare AI research articles.

Guidelines:

- Use only the information provided.
- Do not invent facts or conclusions.
- Maintain an objective and scientific tone.
- Produce concise and accurate summaries.
- Highlight the main contribution of the study.
- Mention clinical relevance when appropriate.
- Avoid unnecessary technical details.

Return your response using exactly this format:

Summary:
<summary>

Key Takeaway:
<single sentence>
""".strip()
  
  def build_user_prompt(self, article: RankedArticle) -> str:
    # Build the user prompt from a ranked article.
    article = article.article

    authors = ", ".join(article.authors) if article.authors else "Unknown"
    keywords = ", ".join(article.keywords) if article.keywords else "None"
    abstract = article.abstract or "No abstract available."
    published = (
      article.published_at.date().isoformat()
      if article.published_at
      else "Unknown"
    )

    return f"""
Title:
{article.title}

Abstract:
{abstract}

DOI:
{article.doi or "N/A"}

Authors:
{authors}

Keywords:
{keywords}

Published:
{published}

Please generate:

Summary:

Key Takeaway:
""".strip()

  def build_prompts(
    self,
    article: RankedArticle,
  ) -> tuple[str, str]:
    return (
      self.build_system_prompt(),
      self.build_user_prompt(article),
    )
  
  def build(
    self, 
    article: RankedArticle
  ) -> str:
    # Combine system and user prompts.
    system, user = self.build_prompts(article)

    return f"{system}\n\n---\n\n{user}"
