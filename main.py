from HolidayAgent.agents.planner import HolidayPlannerAgent
from HolidayAgent.agents.researcher import HolidayResearcherAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


planner = HolidayPlannerAgent()
researcher = HolidayResearcherAgent()

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")


termination = TextMentionTermination("APPROVE")
team = RoundRobinGroupChat([planner.plan_trip(), researcher.research_destinations()], termination_condition=termination)

if __name__ == "__main__":
    response = asyncio.run(team.run(task="I want to two day trip to mayanoor,karur with the budget of 50000. Can you help me plan it?"))
    print("Final response:", response)
