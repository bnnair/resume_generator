##  AI-powered content optimization for resume section enhancements
# Template Method Pattern
from abc import ABC, abstractmethod
from typing import Dict, List
from pydantic import BaseModel
from logging_config import logger
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from services.llm.llm_manager import AIAdapter
from models.resume import Skill

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

class SkillList(BaseModel):
    skills: List[Skill]

class SectionOptimizer(ABC):
    def __init__(self, model_type: str):
        # Call the LLM to analyze the jd
        self.aiadapter = AIAdapter(model_type)
        logger.debug(f"adapter : {self.aiadapter}")        

    
    def optimize_section(self, context: 'OptimizationContext') -> Dict:
        section_data = self._extract_data(context)
        if self._needs_optimization(section_data):
            optimized = self._apply_optimization(section_data, context.jd_analysis)
            return self._format_output(optimized)
        return section_data
    
    @abstractmethod
    def _extract_data(self, context: 'OptimizationContext') -> Dict:
        pass
    
    @abstractmethod
    def _needs_optimization(self, section_data: Dict) -> bool:
        pass
    
    @abstractmethod
    def _apply_optimization(self, section_data: Dict, jd_analysis: Dict) -> Dict:
        pass
    
    def _format_output(self, optimized_data: Dict) -> Dict:
        return optimized_data

# Builder Pattern
class OptimizationContext:
    def __init__(self, resume_data: Dict, jd_analysis: Dict):
        self.resume_data = resume_data
        self.jd_analysis = jd_analysis
    
    def new_with_section(self, section_data: Dict):
        return OptimizationContext(
            {"current_section": section_data},
            self.jd_analysis
        )

# Concrete Optimizers
class SummaryOptimizer(SectionOptimizer):
    def _extract_data(self, context):
        summary = context.resume_data['current_section'].summary
        return summary
        
    def _needs_optimization(self, data):
        return True
    
    def _apply_optimization(self, data, jd_analysis):
        
        prompt = f'''
        Generate a professional resume summary optimized for the target job by following these steps:

        1. Analyze the job requirements: Focus on {jd_analysis.technical_skills} and {jd_analysis.requirements}

        2. Optimization criteria:
        - Concise: Keep strictly under 100 words
        - Relevant: Naturally integrate these keywords: {", ".join(jd_analysis.keywords)}
        - Format: Plain text only, no markdown or special characters (*, **, etc.)
        - Layout: Full sentences with proper punctuation

        3. Input data to refine:
        {data}

        Output only the revised summary text without any additional commentary. Adhere strictly to these formatting rules:
        - No bullet points
        - No asterisks or other symbols
        - No section headers
        - No quotation marks'''
        optimized = self.aiadapter.invoke(prompt)
        logger.info(f"Optimized in apply optimization method  ----: {optimized}")
        return optimized


# Concrete Optimizers
class ExperienceOptimizer(SectionOptimizer):
    def _extract_data(self, context):
        position = context.resume_data['current_section'].position
        resp = context.resume_data['current_section'].responsibilities 
        return {"position": position, "responsibilities": resp}
        
    def _needs_optimization(self, data):
        return data['responsibilities'] is not None and "Project done during Mtech" not in data['responsibilities'][0]
    
    def _apply_optimization(self, data, jd_analysis):
        
        prompt = f'''
        Optimize the responsibilities data for the role of `{data['position']}` by incorporating relevant technical skills 
        (`{jd_analysis.technical_skills}`) and requirements (`{jd_analysis.requirements}`). Use keywords from 
        `{jd_analysis.keywords}` naturally to refine the list. Make sure that based on the role,  the responsibilities should 
        match like if role is tech lead, then mostly responsibilities will include, technology, design, architecture, code reviews,
        unit testing, defect resolution, etc..  
        - Add, remove, or modify responsibilities to strictly align with the position and the job description.  
        - Keep the revisions concise and job-specific.  
        - Ensure the revised list is numbered and does not include any additional text or characters. 
        - Keep the list to 5 to 6 points. Make sure that there is no extra characters like ** or something.
        Original Responsibilities:  
        {data['responsibilities']}  
        Revised Responsibilities: '''
        optimized = self.aiadapter.invoke(prompt)
        # Split the string into a list of sentences based on the newline character
        optimized = optimized.strip().split('\n')        
        logger.info(f"Optimized in apply optimization method  ----: {optimized}")
        return optimized

class SkillOptimizer(SectionOptimizer):
    def _extract_data(self, context):
        skills = context.resume_data['current_section']
        # Split each skill's description into parts, clean whitespace, filter blanks, then join all parts
        cleaned_parts = [part.strip() for skill in skills for part in skill.description.split(",") if part.strip()]
        strdesc = ",".join(cleaned_parts)
        desc =  [strdesc]
        return desc
    
    def _needs_optimization(self, data):
        return True
    
    def _apply_optimization(self, data, jd_analysis):
        parser = JsonOutputParser(pydantic_object=SkillList)
        
        prompt =  PromptTemplate(
        template = """
        Analyze the provided job description (JD) and context to extract relevant skills. Consolidate the skills \
        from both sources into a single list, eliminating duplicates. 
        Then, Combine and group these skills into high-level, relevant categories such as:
        - Project Management
        - Data Science
        - Cloud Computing
        - Software Development
        - Communication

        Present the output in a structured format:
        High-level category
        Comma-separated skills under that category
        Ensure the output is concise, well-organized, and free of unwanted details.
        Job Description (JD): {jd}
        Context: {context}
        Format Instructions: {format_instructions}
        """,
        input_variables=["context", "jd"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        
        logger.info("calling aiadapter invoke method")
        response = self.aiadapter.invoke(prompt.format(context=data, jd=jd_analysis.technical_skills))
        logger.info(f"ai response : {response}") 
        parser_response = parser.invoke(response)   
        logger.info(f"parser response : {parser_response}")   

        skillsOuput = [Skill(**skill_data) for skill_data in parser_response["skills"]]         
        logger.info(f"skills : {skillsOuput}")
        return skillsOuput

# Chain of Responsibility Pattern
class OptimizationHandler(ABC):
    _next_handler = None
    
    def set_next(self, handler):
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, context: 'OptimizationContext'):
        pass

class ExperienceHandler(OptimizationHandler):
    def __init__(self, optimizer: SectionOptimizer):
        self.optimizer = optimizer
    
    def handle(self, context):
        
        for exp in context.resume_data.experiences:
                new_resp = []
                new_resp=self.optimizer.optimize_section(context.new_with_section(exp))
                if isinstance(new_resp, dict): 
                    exp.responsibilities = new_resp["responsibilities"]
                else:
                    exp.responsibilities = new_resp
        
        if self._next_handler:
            self._next_handler.handle(context)

class SummaryHandler(OptimizationHandler):
    def __init__(self, optimizer: SectionOptimizer):
        self.optimizer = optimizer
    
    def handle(self, context):
        summary = context.resume_data.summary
        updated_summary=self.optimizer.optimize_section(
            context.new_with_section(summary))
        context.resume_data.summary.summary = updated_summary
        
        if self._next_handler:
            self._next_handler.handle(context)

class SkillHandler(OptimizationHandler):
    def __init__(self, optimizer: SectionOptimizer):
        self.optimizer = optimizer
    
    def handle(self, context):
        skills =  context.resume_data.skills
        # for skill in skills:
        updated_skills = self.optimizer.optimize_section(context.new_with_section(skills))
        context.resume_data.skills = updated_skills

        if self._next_handler:
            self._next_handler.handle(context)
