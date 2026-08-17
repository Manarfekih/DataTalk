from datatalk.evaluation.metrics import (
    SQLNormalizer,
    EvaluationMetrics,
)

from datatalk.evaluation.models import EvaluationResult



def test_sql_normalizer() -> None:
    sql = """

    SELECT *
    FROM customers;

    """

    normalized = SQLNormalizer.normalize(sql)

    assert normalized == "select * from customers"



def test_text_to_sql_accuracy() -> None:
    results = [
        EvaluationResult(
            case_id="1",
            question="test",
            generated_sql="SELECT * FROM customers;",
            expected_sql="select * from customers",
        )
    ]

    score = EvaluationMetrics.text_to_sql_accuracy(results)

    assert score == 1.0



def test_execution_accuracy() -> None:
    results = [
        EvaluationResult(
            case_id="1",
            question="test",
            execution_correct=True,
        )
    ]

    score = EvaluationMetrics.execution_accuracy(results)

    assert score == 1.0
