from datatalk.agents.generation_agent import GenerationAgent
from datatalk.llm import get_llm


def test_generation_agent():

    llm = get_llm()

    agent = GenerationAgent(
        llm=llm
    )


    result = agent.generate(

        question="How many customers are there?",

        explanation=(
            "There are 91 customers "
            "registered in the system."
        ),

        columns=[
            "count"
        ],

        rows=[
            {
                "count": 91
            }
        ],
    )


    assert result is not None


    assert result.summary


    assert isinstance(
        result.insights,
        list
    )


    assert len(
        result.insights
    ) > 0


    assert isinstance(
        result.follow_up_questions,
        list
    )


    assert len(
        result.follow_up_questions
    ) > 0