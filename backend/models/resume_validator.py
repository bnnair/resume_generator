# src/domain/entities/resume_validator.py
from abc import ABC, abstractmethod

from typing import Dict, Any, Optional

# Chain of Responsibility Pattern for Validation
class Validator(ABC):
    """Chain of Responsibility pattern for resume validation."""
    _next: Optional['Validator'] = None

    def set_next(self, validator: 'Validator') -> 'Validator':
        self._next = validator
        return validator

    @abstractmethod
    def validate(self, data: Any) -> tuple:
        pass

    def _next_validate(self, data: Any) -> tuple:
        if self._next:
            return self._next.validate(data)
        return (True, "Validation passed")

class ResumeStructureValidator(Validator):
    """Validates the structure of the resume."""
    def validate(self, resume: Dict) -> tuple:
        required_fields = ['summary','experiences', 'skills']
        for field in required_fields:
            if field not in resume:
                return (False, f"Missing required field: {field}")
        return self._next_validate(resume)

class ResumeContentNormalizer(Validator):
    """Normalizes the content of the resume."""
    def validate(self, resume: Dict) -> tuple:
        return self._next_validate(resume)
