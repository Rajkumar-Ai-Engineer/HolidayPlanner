from HolidayAgent.core.holiday_exception import HolidayAgentException
from HolidayAgent.core.logger import logging
import sys 
import os 
from langchain_community.utilities import GoogleSerperAPIWrapper


def serper_tool(query: str):
    """ Serper tool to search on web  related to the hotel availability and other travel-related information."""
    try:
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            raise HolidayAgentException("SERPER_API_KEY is not set in environment variables.")
        client = GoogleSerperAPIWrapper(serper_api_key=api_key)
        return client.run(query)
    except Exception as e:
        logging.error(f"Error in Serper tool: {str(e)}")
        raise HolidayAgentException(e,sys)