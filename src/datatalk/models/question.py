from pydantic import BaseModel


class QuestionUnderstandingOutput(BaseModel):

    original_question: str = ""

    corrected_question: str

    intent: str

    needs_clarification: bool

    clarification_question: str | None = None