from fastapi import APIRouter, UploadFile, File, HTTPException,  Depends, status
import os
import json
from pathlib import Path
from logging_config import logger
import base64

from utils.utils import save_to_jsonfile, save_jobDesc
from utils.input_parser import InputParser
from models.resume import Resume
from models.jobdesc import JDList
from services.generator.resume_service import ResumeService

from services.analyzer.jd_analyzer import JDAnalyzer
from services.optimizer.optimizer_manager   import SectionOptimizationManager
from services.generator.style_manager import StyleManager
from services.generator.resume_generator import ResumeGenerator
from services.generator.manager_facade import FacadeManager


 
resume_router = APIRouter(prefix="/resumes", tags=['resumes'])
   
# Dependency Injection: create an instance of ResumeService
def get_resume_service():
    return ResumeService()


folder_path = Path(__file__).resolve().parents[2]
file_path=os.path.join(folder_path, "data", "generated_cvjson")
pdf_file_path = os.path.join(folder_path,"data", "generated_cvpdf")
jd_file_name=os.path.join(folder_path, "data", "joblist.json")


@resume_router.post(
    "/upload-resume",
    response_model=Resume, 
)
async def upload_resume(file:UploadFile = File(...),
                        res_service : ResumeService = Depends(get_resume_service)):
    resume_file = os.path.join(file_path, "resume.json")
    response = await res_service.upload_resume(file)
    try:
        save_to_jsonfile(response, resume_file)
    except Exception as e:
        logger.error(f"Exception occured during saving the json resume file : {e}")
        
    return Resume(**response)  
        

@resume_router.get(
    "/get-all-resumes",
) 
async def get_all_resumes():
    logger.info(f" inside the get all resume method in main")
    json_file_list = []
    data = ""
    try:
        for file_name in os.listdir(file_path):
            if file_name.endswith(".json"):
                json_file_list.append({"name":file_name})
                
        logger.debug(f"resume file path ----> {json_file_list}")        
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Error getting the json list: {str(e)}"
        )  
    return json_file_list


@resume_router.get(
    "/get-json-resume/{cv_name}",
) 
async def get_json_resume(cv_name: str):
    logger.info(f" inside the get json resume method in main")
    # logger.debug(f"Resume model dump json ===> {Resume}")
    # folder_path = Path(__file__).resolve().parents[2]
    resume_file=os.path.join(file_path, cv_name)
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
    "/save-resume/{cv_name}",
) 
async def save_resume(json_resume: dict, cv_name :str):
    logger.info(f" inside the save json resume method in main")
    resume_file=os.path.join(file_path, cv_name)
    pdf_name = cv_name.split(".")[0]+".pdf"
    logger.debug(f"pdf name ----{pdf_name}")
    pdf_resume_file = os.path.join(pdf_file_path,pdf_name)
    logger.debug(f"Saving the json resume ===> {json_resume}")
    try:
        save_to_jsonfile(json_resume,resume_file)
        ## Generate the PDF from the json file
        style_manager = StyleManager()
        resume_generator = ResumeGenerator()
        facade_manager = FacadeManager(
        style_manager, resume_generator, Resume(**json_resume))
        
        facade_manager.choose_style()
        resume_pdf_base64 = facade_manager.pdf_base64()
        
        with open(pdf_resume_file, "wb") as f:
            f.write(base64.b64decode(resume_pdf_base64))
        
        
    except Exception as e:
        logger.error(f"Exception occured during saving the json resume file : {e}")


@resume_router.get(
    "/gen-json-resume-per-jd/{selectedJDName}",
) 
async def gen_json_resume_per_jd(selectedJDName: str):
    MODEL_TYPE = 'deepseek'
    logger.info(f" inside the generate json resume method in main")
    resume_file=os.path.join(file_path, "resume.json")
    logger.debug(f"resume file path ----> {resume_file}")
    data = ""
    try:
        company = selectedJDName.split("_")[0]
        title =selectedJDName.split("_")[1]
        logger.debug(f"company=={company} and title=={title}")
        parser = InputParser()
        success, message, resume, jd = parser.parse_inputs(resume_file, jd_file_name)
        
        if success:
            print("Processing successful!")
            print("Normalized Resume:", resume)
            print("Processed JD:", jd)
        else:
            print("Error:", message)
        
        jd_text = ""
        for jdItem in jd['jobDescription']:
            logger.debug(f"jditem from response -- {jdItem}")
            
            origCompany = company.replace("$", "").lower()
            origJobTitle = title.replace("$", "").lower()
            jdCompany = jdItem['company'].strip().replace(" ", "").lower()
            jdTitle = jdItem['jobTitle'].strip().replace(" ", "").lower()
            logger.debug(f"origcomp---{origCompany} and origTitle---{origJobTitle}")
            logger.debug(f"jdcompany---{jdCompany} and jdTitle---{jdTitle}")
            logger.debug(f"(origCompany== jdItem['company'])====={(origCompany== jdCompany)}")
            logger.debug(f"(origJobTitle == jdItem['jobTitle'])==={(origJobTitle == jdTitle)}")
            if (origCompany== jdCompany) and (origJobTitle == jdTitle):
                logger.debug("inside the if loop for jditem")
                jd_text =jdItem['jobDesc']
                jdItem['resumeGenerated'] = True
                break

        logger.debug(f"jd updated for resume generated--- { jd}")                
        analyzer = JDAnalyzer()
        result = analyzer.analyze(jd_text)
        
        logger.info(f"Keywords:{result.keywords}")
        logger.info(f"Requirements:{result.requirements}")
        logger.info(f"Techincal SKills:{result.technical_skills}")

        optimizer = SectionOptimizationManager(llm_model_type=MODEL_TYPE)
        optimized_resume = optimizer.optimize_resume(resume.model_copy(), result)
        
        print("Original Resume:", resume)
        print("Optimized Resume:", optimized_resume)

        ##SAve the optimized resume as json
        save_to_jsonfile(optimized_resume.model_dump(), os.path.join(file_path, f"cv_{company}_{title}.json"))        

        for jdItem in jd['jobDescription']:
            logger.debug(f"jditem from response -- {jdItem}")
        save_jobDesc(JDList(**jd),jd_file_name)
    except Exception as e:
        logger.error(f"Exception occurred while generating the resume: {str(e)}")
        return False
    
    return True