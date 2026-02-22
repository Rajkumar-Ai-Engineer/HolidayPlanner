from autogen_agentchat.agents import AssistantAgent,UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
import asyncio

api_key = os.getenv("GROQ_API_KEY")

llm = OpenAIChatCompletionClient(
        model="openai/gpt-oss-120b",
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        temperature=0.2,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "structured_output": False,
            "family": "unknown",
        }
        
)

assistant_agent = AssistantAgent(
    name="Travel_Planner",
    model_client=llm,
    system_message="You are a helpful travel assistant. You can help users plan trips, find destinations, and provide travel recommendations.",
)

research_agent = AssistantAgent(
    name="Travel_Researcher",
    model_client=llm,
    system_message="""You are a travel fact-checker.
        Check for:
        - Accuracy of attractions
        - Realistic travel time
        - Opening hours
        - Cost estimates

        If itinerary looks good, say APPROVE.
        Otherwise suggest corrections.
        """

)

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination

termination = TextMentionTermination("APPROVE")

# Create the team.
team = RoundRobinGroupChat([assistant_agent,research_agent], termination_condition=termination,max_turns=6)





response = asyncio.run(team.run(task="I want to two day trip to Paris. Can you help me plan it?"))
print("Final response:", response)
