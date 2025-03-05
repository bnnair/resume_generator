# backend/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException,  Depends,Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import json
from dotenv import load_dotenv
from pathlib import Path
from logging_config import logger


from utils.pdf_parser import load_pdf
from utils.utils import save_to_jsonfile, save_jobDesc

from models.resume import Resume
from models.jobdesc import JDList

from services.resume_service import ResumeService

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Resume Generator",
    description="API for resume enhancement and generation",
    version="1.0.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], ## for production, this should be limited to specific domains
    allow_methods=["*"], ## for production, this should be limited to specific methods
    allow_headers=["*"], ## for production, this should be limited to specific headers
    allow_credentials=True,
)

# Custom exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
    
# Dependency Injection: create an instance of ResumeService
def get_resume_service():
    return ResumeService()


@app.post(
    "/api/upload-resume",
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
        

@app.get(
    "/api/get-json-resume",
) 
async def get_json_resume():
    logger.info(f" inside the get json resume method in main")
    # logger.debug(f"Resume model dump json ===> {Resume}")
    folder_path = Path(__file__).resolve().parent
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


@app.get(
    "/api/get-jd-list",
) 
async def get_jd_list():
    logger.info(f" inside the get get JD List method in main")
    folder_path = Path(__file__).resolve().parent
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


@app.put(
    "/api/save-resume",
) 
async def save_resume(json_resume: dict):
    logger.info(f" inside the save json resume method in main")
    logger.debug(f"Saving the json resume ===> {json_resume}")
    try:
        save_to_jsonfile(json_resume)
    except Exception as e:
        logger.error(f"Exception occured during saving the json resume file : {e}")


@app.put(
    "/api/save-jobdesc",
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

        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000))
    )
