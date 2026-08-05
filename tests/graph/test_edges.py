from datatalk.graph.edges import execution_router


class FakeExecution:

    def __init__(self, success):
        self.success = success



def test_execution_router_success():


    state = {

        "execution":
            FakeExecution(True)

    }


    result = execution_router(
        state
    )


    assert result == "success"





def test_execution_router_failure():


    state = {

        "execution":
            FakeExecution(False)

    }


    result = execution_router(
        state
    )


    assert result == "retry"





def test_execution_router_missing_execution():


    state = {}


    result = execution_router(
        state
    )


    assert result == "retry"