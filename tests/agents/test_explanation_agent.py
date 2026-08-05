from datatalk.agents.explanation_agent import ExplanationAgent

from datatalk.llm import get_llm

from datatalk.models.explanation import ExplanationOutput



def test_explanation_agent():

    # Create LLM provider

    llm = get_llm()


    # Create agent

    agent = ExplanationAgent(
        llm=llm
    )


    # Fake SQL result

    result = agent.explain(

        question="How many customers are there?",

        columns=[
            "total_customers"
        ],

        rows=[
            {
                "total_customers": 91
            }
        ],

    )


    print("\nExplanation:")
    print(result.explanation)



    assert isinstance(
        result,
        ExplanationOutput
    )


    assert result.explanation
