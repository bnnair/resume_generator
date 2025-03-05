from logging_config import logger
from pathlib import Path
import json

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