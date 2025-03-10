
from abc import ABC, abstractmethod
# from dataclasses import dataclass
from typing import List
from pydantic import BaseModel
from logging_config import logger

from services.llm.llm_manager import AIAdapter

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate



class JDAnalysisResult(BaseModel):
    keywords: List[str]
    requirements: List[str]
    technical_skills: List[str]

# Strategy Pattern for different analysis approaches
class AnalysisStrategy(ABC):
    @abstractmethod
    def analyze(self, text: str) -> dict:
        pass

class JDSummarizeStrategy(AnalysisStrategy):
    def __init__(self):
        pass
        
    def analyze(self, text: str) -> dict:
        
        MODEL_TYPE = "deepseek"
        # Call the LLM to analyze the jd
        aiadapter = AIAdapter(MODEL_TYPE)
        logger.debug(f"adapter : {aiadapter}")

        parser = JsonOutputParser(pydantic_object=JDAnalysisResult)

        prompt = PromptTemplate(
        template="you are a technical recruiter with knowledge on how to analyze a \
             job description commonly used by ATS. I would want you to analyze the job \
             description given and then categorize them exactly into the specified\n{format_instructions}\n{context}\n",
        input_variables=["context"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        logger.info("calling aiadapter invoke method")
        response = aiadapter.invoke(prompt.format(context=text))
        parser_response = parser.invoke(response)            
        logger.info(f"response : {parser_response}")   
        return parser_response


