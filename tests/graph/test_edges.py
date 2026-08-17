from datatalk.graph.edges import execution_router, retry_router


class FakeExecution:
    def __init__(self, success):
        self.success = success



def test_execution_router_success():
    state = {
        "execution": FakeExecution(True)
    }

    result = execution_router(state)

    assert result == "success"



def test_execution_router_failure():
    state = {
        "execution": FakeExecution(False),
        "retry_count": 0,
        "max_retries": 2,
    }

    result = execution_router(state)

    assert result == "retry"



def test_execution_router_exhausted_retries():
    state = {
        "execution": FakeExecution(False),
        "retry_count": 2,
        "max_retries": 2,
    }

    result = execution_router(state)

    assert result == "explain"



def test_execution_router_missing_execution():
    state = {}

    result = execution_router(state)

    assert result == "retry"



def test_retry_router_continue():
    state = {
        "retry_count": 0,
        "max_retries": 2,
    }

    result = retry_router(state)

    assert result == "execute"



def test_retry_router_stop():
    state = {
        "retry_count": 2,
        "max_retries": 2,
    }

    result = retry_router(state)

    assert result == "explain"
