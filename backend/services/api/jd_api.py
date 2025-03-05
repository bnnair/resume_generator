from fastapi import APIRouter, HTTPException, status
import os
import json
from pathlib import Path
from logging_config import logger
from utils.utils import  save_jobDesc
from models.jobdesc import JDList


jd_router = APIRouter(prefix="/jds", tags=['jobDesc'])

@jd_router.get(
    "/get-jd-list",
) 
async def get_jd_list():
    logger.info(f" inside the get get JD List method in main")
    folder_path = Path(__file__).resolve().parents[2]
    jdFile=os.path.join(folder_path, "data", "joblist.json")
    logger.debug(f"JD file path ----> {jdFile}")
    data = ""
    try:
        if os.path.exists(jdFile):
            with open(jdFile, "r", encoding="utf8") as file:
                # logger.debug(file)
                data = json.load(file)
                logger.debug(f"data of JD===> { data}")
                
    except FileNotFoundError:
        logger.error("The file does not exist.")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Error getting the resume: {str(e)}"
        )  
    return JDList(**data)


@jd_router.put(
    "/save-jobdesc",
) 
async def save_jobdesc(jd: JDList):
    logger.info(f" inside the save jobdesc method in main")
    logger.debug(f"Saving the job desc ===>{jd}")
    try:
        save_jobDesc(jd)
        return "success"
    except Exception as e:
        logger.error(f"Exception occured during saving the jd file : {e}")
        return "Failure"