from __future__ import annotations

import logging

from ..llm.base import BaseLLMProvider
from ..models.question import QuestionUnderstandingOutput
from ..prompts.question_understanding import QUESTION_UNDERSTANDING_PROMPT


logger = logging.getLogger(__name__)


class QuestionUnderstandingAgent:

    def __init__(
        self,
        llm: BaseLLMProvider,
    ) -> None:

        self.llm = llm


    def process(
        self,
        question: str,
    ) -> QuestionUnderstandingOutput:

        if not question.strip():
            raise ValueError(
                "Question cannot be empty"
            )


        logger.info(
            "Understanding user question: %s",
            question,
        )


        prompt = QUESTION_UNDERSTANDING_PROMPT.format(
            question=question
        )


        result = self.llm.generate_structured(
            prompt=prompt,
            response_model=QuestionUnderstandingOutput,
            temperature=0.1,
        )


        logger.info(
            "Question intent detected: %s",
            result.intent,
        )


        return result