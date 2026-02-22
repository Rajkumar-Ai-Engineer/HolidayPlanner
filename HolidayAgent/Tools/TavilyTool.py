from langchain_tavily import TavilySearch
from HolidayAgent.core.holiday_exception import HolidayAgentException
from HolidayAgent.core.logger import logging
import sys 
import os 

def tavily_tool(query: str):
    """ Tavily tool to search on web  related to the hotel, destination, activities, and other travel-related information."""
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise HolidayAgentException("TAVILY_API_KEY is not set in environment variables.")
        client = TavilySearch(api_key=api_key)
        return client.invoke(query)
    except Exception as e:
        logging.error(f"Error in Tavily tool: {str(e)}")
        raise HolidayAgentException(e,sys)