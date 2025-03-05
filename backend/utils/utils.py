from loguru import logger
import os, sys
from app_config import MINIMUM_LOG_LEVEL
from models.resume import Resume
from pathlib import Path
import json
from models.jobdesc import JDList

log_folder = 'log'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Configure the log path
log_file = os.path.join(log_folder, 'app_log.log')

if MINIMUM_LOG_LEVEL in ["DEBUG", "TRACE", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    logger.remove()
    logger.add(sys.stderr, level=MINIMUM_LOG_LEVEL)
    # Add a sink to log to a file
    logger.add(log_file, rotation="5 MB", format="{time} {level} {message}")
else:
    logger.warning(
        f"Invalid log level: {MINIMUM_LOG_LEVEL}. Defaulting to DEBUG.")
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")
    
    
    
def save_to_jsonfile(resume: dict):
    
    json_resume_folder = Path(__file__).resolve().parent.parent
    logger.debug(f"json resume folder----> {json_resume_folder}")
    json_resume_file = json_resume_folder.joinpath("data", "resume.json")    
    logger.debug(f"json resume file --------> {json_resume_file}")
    
    # Save to a JSON file
    with open(json_resume_file, "w", encoding="utf8") as json_file:
        json.dump(resume, json_file, indent=4, ensure_ascii=False)  # `indent` for pretty formatting


def save_jobDesc(jobDesc : dict):
    jd_folder = Path(__file__).resolve().parent.parent
    logger.debug(f"jd folder----> {jd_folder}")
    jd_file = jd_folder.joinpath("data", "joblist.json")    
    logger.debug(f"job Desc file --------> {jd_file}")
    logger.debug(f"job Desc file --------> {jobDesc.dict()}")
   
    with open(jd_file, "w", encoding="utf8") as jd_file:
           json.dump(jobDesc.dict(), jd_file, indent=4, ensure_ascii=False) 