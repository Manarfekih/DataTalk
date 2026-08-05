from pydantic import BaseModel


class RetryConfig(BaseModel):

    max_attempts:int = 3

    min_confidence:float = 0.7