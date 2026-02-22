from HolidayAgent.core.holiday_exception import HolidayAgentException
from HolidayAgent.core.logger import logging
import sys 
import os 
import googlemaps
from datetime import datetime

def google_map_tool(source: str, destination: str):
    """ Google Map tool to get distance and duration between source and destination."""
    try:
        api_key = os.getenv("MAP_API_KEY")
        client = googlemaps.Client(key=api_key)
        result = client.distance_matrix(origins=source,destinations=destination,mode="driving",departure_time=datetime.now())
        return result
    except Exception as e:
        logging.error(f"Error in Google Map tool: {str(e)}")
        raise HolidayAgentException(e,sys)