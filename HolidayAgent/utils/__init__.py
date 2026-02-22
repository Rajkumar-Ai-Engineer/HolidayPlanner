import os 
from HolidayAgent.core.holiday_exception import HolidayAgentException
from HolidayAgent.core.logger import logging
import sys

def load_txt(file_path: str) -> str:
    try:
        
        with open(file_path, "r") as file:
            content = file.read()
        return content
    except Exception as e:
        logging.error(f"Error in loading txt file: {str(e)}")
        raise HolidayAgentException(e,sys)