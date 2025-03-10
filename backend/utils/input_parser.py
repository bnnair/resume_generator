# src/application/presentation/api/input_parser.py
import json
from typing import Dict
from models.resume_builder import ResumeBuilder
from models.resume import Resume

from models.jd_validator import (
    ChainValidator, JDStructureValidator, JDContentValidator
)
from logging_config import logger



class InputParser:
    """Facade pattern for parsing and validating inputs."""
    def __init__(self):
        self._resume_builder = ResumeBuilder()
        self._jd_validator = ChainValidator([
            JDStructureValidator(),
            JDContentValidator()
        ])

    def parse_inputs(self, resume_file: str, job_desc_file: str) -> tuple:
        """Facade entry point for parsing inputs."""
        try:
            with open(resume_file, "r", encoding="utf8") as file:
                logger.debug(file)
                resume_data = json.load(file)            
        except FileNotFoundError:
             return (False, "File does not exist", None, None)
        except json.JSONDecodeError:
            return (False, "Invalid JSON format in resume", None, None)
        except Exception as e:
            return (False, f"Error getting the resume: {str(e)}", None, None)
        
        # Process resume
        valid_resume, msg, resume = self._build_resume(resume_data)
        if not valid_resume:
            return (False, msg, None, None)

        logger.info(f"jd file name inside parse -- {job_desc_file}")

        try:
            with open(job_desc_file, "r", encoding="utf8") as file:
                logger.debug(file)
                job_desc_data = json.load(file)            
        except FileNotFoundError:
             return (False, "File does not exist", None, None)
        except json.JSONDecodeError:
            return (False, "Invalid JSON format in resume", None, None)
        except Exception as e:
            return (False, f"Error getting the JD: {str(e)}", None, None)

        logger.debug(f"job desc data from load - {job_desc_data}")
        jd_list = []
        for dataList in job_desc_data.get("jobDescription"):
            logger.debug(f"datalist ====> {dataList}")
            for keys in dataList:
                logger.debug(f"keys -----> {keys}")
                if keys =="jobDesc":
                    logger.debug(f"inside the if loop")
                    job_description = dataList[keys]
                    logger.debug(f"job description-----> {job_description}")
                    
                    # Process job description
                    valid_jd, jd_msg, processed_jd = self._jd_validator.process(job_description)
                    logger.debug(f"processed jd -----> {processed_jd}")
                    dataList[keys] = processed_jd
                    jd_list.append(dataList)
                    logger.debug(f"jd list ----->{jd_list }")
                    
                    if not valid_jd:
                        return (False, jd_msg, None, None)
        # logger.debug(f'resume--------> {resume}')

        resumeModel = Resume(**resume)
        logger.debug(f"resumeModel==============> {resumeModel}")
        
        job_desc_data["jobDescription"] = jd_list
        return (True, "Inputs validated successfully", resumeModel, job_desc_data)

    def _build_resume(self, raw_data: Dict) -> tuple:
        """Uses builder pattern to construct resume object."""
        builder = self._resume_builder
        for section, content in raw_data.items():
            builder.add_section(section, content)
        return builder.validate_normalize()
