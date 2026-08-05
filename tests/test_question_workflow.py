from __future__ import annotations

import pytest

from datatalk.core.container import container
from datatalk.models import QueryResult


@pytest.fixture(scope="module")
def workflow():

    """
    Initialize application container once
    for all workflow tests.
    """

    container.initialize()

    return container.query_workflow



# ==========================================================
# Test 1: Normal user question
# ==========================================================

def test_normal_question(workflow):


    question = (
        "How many customers are there?"
    )


    result = workflow.ask(
        question
    )


    assert isinstance(
        result,
        QueryResult
    )


    assert result.sql_query is not None


    assert "SELECT" in result.sql_query.upper()


    assert result.execution.success


    assert result.execution.row_count == 1



# ==========================================================
# Test 2: Bad grammar / typo correction
# ==========================================================

def test_malformed_question_correction(workflow):


    question = (
        "how many custmers do we hav"
    )


    result = workflow.ask(
        question
    )


    assert isinstance(
        result,
        QueryResult
    )


    assert result.execution.success


    assert result.sql_query


    assert (
        "customer"
        in result.sql_query.lower()
    )



# ==========================================================
# Test 3: Customer count expected value
# ==========================================================

def test_customer_count_result(workflow):


    question = (
        "Give me the number of customers"
    )


    result = workflow.ask(
        question
    )


    assert result.execution.success


    rows = result.execution.rows


    assert len(rows) == 1


    assert (
        "total_customers"
        in rows[0]
    )


    assert (
        rows[0]["total_customers"]
        > 0
    )



# ==========================================================
# Test 4: Unknown request should not crash
# ==========================================================

def test_unknown_question(workflow):


    question = (
        "What is the weather today?"
    )


    result = workflow.ask(
        question
    )


    assert isinstance(
        result,
        QueryResult
    )


# ==========================================================
# Test 5: Empty question validation
# ==========================================================

def test_empty_question(workflow):


    with pytest.raises(
        Exception
    ):

        workflow.ask("")