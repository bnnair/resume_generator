# Decorator Pattern
import json
from typing import Dict
from services.optimizer.section_optimizer import (
    SectionOptimizer, ExperienceOptimizer, SkillOptimizer , SummaryHandler, SummaryOptimizer,
    ExperienceHandler, SkillHandler, OptimizationContext
    )

class CachingDecorator(SectionOptimizer):
    def __init__(self, optimizer: SectionOptimizer, cache: Dict):
        super().__init__(optimizer.llm)
        self.optimizer = optimizer
        self.cache = cache
    
    def optimize_section(self, context):
        cache_key = f"{context.section_type}:{json.dumps(context.resume_data)}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        result = self.optimizer.optimize_section(context)
        self.cache[cache_key] = result
        return result



# Facade Pattern
class SectionOptimizationManager:
    def __init__(self, llm_model_type: str):
        self.llm_model_type = llm_model_type
        self.handler_chain = self._create_chain()
    
    def _create_chain(self):
        experience_opt = ExperienceOptimizer(self.llm_model_type)
        skill_opt = SkillOptimizer(self.llm_model_type)
        summary_opt = SummaryOptimizer(self.llm_model_type)
        
        experience_handler = ExperienceHandler(experience_opt)
        skill_handler = SkillHandler(skill_opt)
        summary_handler = SummaryHandler(summary_opt)
        
        
        summary_handler.set_next(experience_handler) 
        experience_handler.set_next(skill_handler)

        return summary_handler
    
    def optimize_resume(self, resume_data: Dict, jd_analysis: Dict) -> Dict:
        context = OptimizationContext(resume_data, jd_analysis)
        self.handler_chain.handle(context)
        return context.resume_data
