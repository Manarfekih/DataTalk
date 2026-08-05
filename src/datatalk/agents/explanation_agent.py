from __future__ import annotations

import json
import logging
import time

from ..llm.base import BaseLLMProvider

from ..models.explanation import ExplanationOutput

from ..prompts.explanation import EXPLANATION_PROMPT


logger = logging.getLogger(__name__)


class ExplanationAgent:
    """
    Converts SQL execution results into
    human-readable business explanations.
    """



    def __init__(
        self,
        llm: BaseLLMProvider,
    ) -> None:

        self._llm = llm



    def explain(
        self,
        *,
        question: str,
        columns: list[str],
        rows: list[dict],
    ) -> ExplanationOutput:


        start = time.perf_counter()



        # No results case

        if not rows:

            return ExplanationOutput(
                explanation=(
                    "No data was found "
                    "for this question."
                )
            )



        formatted_rows = json.dumps(
            rows,
            indent=2,
            default=str,
        )



        prompt = EXPLANATION_PROMPT.format(

            question=question,

            columns=", ".join(columns),

            rows=formatted_rows,

        )



        result = (
            self._llm.generate_structured(

                prompt=prompt,

                response_model=ExplanationOutput,

                temperature=0.2,

            )
        )



        elapsed = (
            time.perf_counter()
            -
            start
        ) * 1000



        logger.info(
            "Explanation generated in %.2f ms",
            elapsed,
        )



        return result