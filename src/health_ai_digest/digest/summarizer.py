from health_ai_digest.digest import (
    ArticleSummaryFormatter,
    PromptBuilder,
)
from health_ai_digest.llm import BaseLLMClient
from health_ai_digest.models import (
    ArticleSummary,
    RankedArticle,
)


class Summarizer:
    # Generates structured summaries for ranked articles.
    def __init__(
        self,
        llm_client: BaseLLMClient,
        prompt_builder: PromptBuilder | None = None,
        formatter: ArticleSummaryFormatter | None = None,
    ) -> None:
        self._llm = llm_client
        self._prompt_builder = prompt_builder or PromptBuilder()
        self._formatter = formatter or ArticleSummaryFormatter()

    def summarize(
        self,
        article: RankedArticle,
    ) -> ArticleSummary:
        # Generate an ArticleSummary from a RankedArticle.
        system_prompt, user_prompt = self._prompt_builder.build_prompts(article)

        response = self._llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        return self._formatter.parse(
            response=response,
            ranked_article=article,
        )
