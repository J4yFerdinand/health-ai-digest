import re

from health_ai_digest.models import ArticleSummary, RankedArticle


class ArticleSummaryFormatter:
    # Parse raw LLM responses into ArticleSummary models.

    def parse(
        self,
        response: str,
        ranked_article: RankedArticle,
    ) -> ArticleSummary:
        """
        Convert a raw LLM response into an ArticleSummary.

        Expected format:

        Summary:
        <summary>

        Key Takeaway:
        <key takeaway>
        """
        response = response.strip()

        if not response:
            raise ValueError("LLM response cannot be empty.")

        summary_match = re.search(
            r"^[ \t]*Summary:[ \t]*$",
            response,
            re.MULTILINE | re.IGNORECASE,
        )

        if summary_match is None:
            raise ValueError("Missing 'Summary:' section.")

        key_takeaway_match = re.search(
            r"^[\t]*Key Takeaway:[ \t]*$", response, re.MULTILINE | re.IGNORECASE
        )

        if key_takeaway_match is None:
            raise ValueError("Missing 'Key Takeaway:' section.")

        summary_part = response[summary_match.end() : key_takeaway_match.start()]

        key_takeaway_part = response[key_takeaway_match.end() :]

        summary = summary_part.strip()
        key_takeaway = key_takeaway_part.strip()

        if not summary:
            raise ValueError("Summary cannot be empty.")

        if not key_takeaway:
            raise ValueError("Key takeaway cannot be empty.")

        return ArticleSummary(
            ranked_article=ranked_article,
            summary=summary,
            key_takeaway=key_takeaway,
        )
