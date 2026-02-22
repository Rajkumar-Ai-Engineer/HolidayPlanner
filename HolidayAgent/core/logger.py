import logging 
import datetime 
import os 

folder_name = "logs"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    
logging.basicConfig(
    filename=os.path.join(folder_name,f"holiday_agent_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"),
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(lineno)d -%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)