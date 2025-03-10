from fastapi import APIRouter, HTTPException, status
import os
import json
from pathlib import Path
from logging_config import logger
from utils.utils import  save_jobDesc
from models.jobdesc import JDList
import copy


folder_path = Path(__file__).resolve().parents[2]
jdFile=os.path.join(folder_path, "data", "joblist.json")

jd_router = APIRouter(prefix="/jds", tags=['jobDesc'])


@jd_router.get(
    "/get-jd-list/{show}",
) 
async def get_jd_list(show :str):
    logger.info(f" inside the get get JD List method in main")
    logger.debug(f"JD file path ----> {jdFile}")
    logger.debug(f"show got from front end---{show}")
    data = ""
    try:
        if os.path.exists(jdFile):
            with open(jdFile, "r", encoding="utf8") as file:
                # logger.debug(file)
                data = json.load(file)
                logger.debug(f"data of JD===> { data}")
        temp_data = copy.deepcopy(data)
        for (index, jd) in enumerate(data['jobDescription']):
            logger.debug(f"{index}---{jd['company']}")
            logger.debug((show == "showFiltered") and jd['resumeGenerated'])
            if (show == "showFiltered") and (jd['resumeGenerated']):
                logger.debug("inside the if coomparison")
                temp_data['jobDescription'].remove(jd)
            logger.debug(f"data1 after ---{temp_data}")
            logger.debug(f"data2 after ---{data}")
    

    except FileNotFoundError:
        logger.error("The file does not exist.")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Error getting the resume: {str(e)}"
        )  
    return JDList(**temp_data)


@jd_router.put(
    "/save-jobdesc",
) 
async def save_jobdesc(jd: JDList):
    logger.info(f" inside the save jobdesc method in main")
    logger.debug(f"jd file path  ===>{jdFile}")
    logger.debug(f"Saving the job desc ===>{jd}")
    try:
        save_jobDesc(jd, jdFile)
        return "success"
    except Exception as e:
        logger.error(f"Exception occured during saving the jd file : {e}")
        return "Failure"