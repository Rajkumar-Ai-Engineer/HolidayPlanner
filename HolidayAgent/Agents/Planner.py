from HolidayAgent.core.holiday_exception import HolidayAgentException
from HolidayAgent.core.logger import logging
import sys
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from HolidayAgent.utils import load_txt
from HolidayAgent.config import MODEL_CONFIG, get_api_key, PROMPTS_DIR

class HolidayPlannerAgent():
    def __init__(self):
        self.llm = OpenAIChatCompletionClient(
            api_key=get_api_key(),
            **MODEL_CONFIG
        )
        self.system_message = load_txt(str(PROMPTS_DIR / "planner_prompt.txt"))
        
    def plan_trip(self):
        try:
            return AssistantAgent(
                name="Travel_Planner",
                model_client=self.llm, 
                system_message=self.system_message
            )
        except Exception as e:
            logging.error(f"Error in creating planner agent: {str(e)}")
            raise HolidayAgentException(e, sys)
