from fastapi import APIRouter, UploadFile, File, HTTPException,  Depends, status
import os
import json
from pathlib import Path
from logging_config import logger

from utils.utils import save_to_jsonfile, save_jobDesc

from models.resume import Resume
from services.resume_service import ResumeService
 
 
resume_router = APIRouter(prefix="/resumes", tags=['resumes'])
   
# Dependency Injection: create an instance of ResumeService
def get_resume_service():
    return ResumeService()


@resume_router.post(
    "/upload-resume",
    response_model=Resume, 
)
async def upload_resume(file:UploadFile = File(...),
                        res_service : ResumeService = Depends(get_resume_service)):
    
    response = await res_service.upload_resume(file)
    try:
        save_to_jsonfile(response)
    except Exception as e:
        logger.error(f"Exception occured during saving the json resume file : {e}")
        
    return Resume(**response)  
        

@resume_router.get(
    "/get-json-resume",
) 
async def get_json_resume():
    logger.info(f" inside the get json resume method in main")
    # logger.debug(f"Resume model dump json ===> {Resume}")
    folder_path = Path(__file__).resolve().parents[2]
    resume_file=os.path.join(folder_path, "data", "resume.json")
    logger.debug(f"resume file path ----> {resume_file}")
    data = ""
    try:
        if os.path.exists(resume_file):
            with open(resume_file, "r", encoding="utf8") as file:
                # logger.debug(file)
                  data = json.load(file)
    except FileNotFoundError:
        logger.error("The file does not exist.")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Error getting the resume: {str(e)}"
        )  
    return data

@resume_router.put(
    "/api/save-resume",
) 
async def save_resume(json_resume: dict):
    logger.info(f" inside the save json resume method in main")
    logger.debug(f"Saving the json resume ===> {json_resume}")
    try:
        save_to_jsonfile(json_resume)
    except Exception as e:
        logger.error(f"Exception occured during saving the json resume file : {e}")
