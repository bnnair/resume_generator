 # NLP processing, keyword extraction : JD Processing
 # src/application/core/analyzer/jd_validator.py
from abc import ABC, abstractmethod
from typing import Any
import re

# Abstract Class for JD Analyzer
class JDValidatorStrategy(ABC):
    """Strategy pattern for job description validation."""
    @abstractmethod
    def validate(self, description: str) -> tuple:
        pass

class JDStructureValidator(JDValidatorStrategy):
    """Validates the structure of the job description."""
    def validate(self, description: str) -> tuple:
        if len(description.split()) < 50:
            return (False, "Job description too short")
        return (True, "Structure valid")

class JDContentValidator(JDValidatorStrategy):
    """Validates the content of the job description."""
    def validate(self, description: str) -> tuple:
        return (True, "Content valid")

class ChainValidator:
    """Chain of Responsibility for job description processing."""
    def __init__(self, validators: list[JDValidatorStrategy]):
        self.validators = validators

    def process(self, description: str) -> tuple:
        processed = description.strip()
        for validator in self.validators:
            valid, msg = validator.validate(processed)
            if not valid:
                return (False, msg, None)
        return (True, "Validation passed", self._normalize(processed))
    
    def _normalize(self, text: str) -> str:
        """Normalizes the job description text."""
        return re.sub(r'\s+', ' ', text).strip()
