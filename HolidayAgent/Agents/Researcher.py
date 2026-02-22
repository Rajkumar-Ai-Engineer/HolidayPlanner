from HolidayAgent.core.holiday_exception import HolidayAgentException
from HolidayAgent.core.logger import logging
import sys
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from HolidayAgent.utils import load_txt
from HolidayAgent.Tools.GoogleMap import google_map_tool
from HolidayAgent.Tools.SerperTool import serper_tool
from HolidayAgent.Tools.TavilyTool import tavily_tool
from HolidayAgent.config import MODEL_CONFIG, get_api_key, PROMPTS_DIR

class HolidayResearcherAgent():
    def __init__(self):
        self.llm = OpenAIChatCompletionClient(
            api_key=get_api_key(),
            **MODEL_CONFIG
        )
        self.system_message = load_txt(str(PROMPTS_DIR / "researcher_prompt.txt"))
        
    def research_destinations(self):
        try:
            return AssistantAgent(
                name="Travel_Researcher",
                model_client=self.llm,
                system_message=self.system_message,
                tools=[tavily_tool, google_map_tool, serper_tool]
            )
        except Exception as e:
            logging.error(f"Error in creating researcher agent: {str(e)}")
            raise HolidayAgentException(e, sys)
