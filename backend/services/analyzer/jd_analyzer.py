# Builder Pattern
from abc import ABC, abstractmethod
from dataclasses import dataclass

from services.analyzer.jd_strategy import (
    JDSummarizeStrategy,JDAnalysisResult
)

# Facade Pattern with Template Method
class JDAnalyzer:
    def __init__(self):
        self.strategies = {
            'result': JDSummarizeStrategy()
        }
       
    def analyze(self, jd_text: str) -> JDAnalysisResult:
        # Strategy Pattern usage
        response  = self.strategies['result'].analyze(jd_text)
        # # Combine all results
        return JDAnalysisResult(**response )

        
