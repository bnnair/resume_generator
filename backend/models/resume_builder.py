# src/application/core/optimizer/resume_builder.py
from typing import Dict
from models.resume_validator import (
    ResumeStructureValidator, ResumeContentNormalizer
)

class ResumeBuilder:
    """Builder pattern for constructing and validating a resume."""
    def __init__(self):
        self._resume = {}
        self._validator_chain = ResumeStructureValidator()
        self._validator_chain.set_next(ResumeContentNormalizer())

    def add_section(self, section: str, data: Dict) -> 'ResumeBuilder':
        self._resume[section] = data
        return self

    def validate_normalize(self) -> tuple:
        valid, msg = self._validator_chain.validate(self._resume)
        if not valid:
            self._resume = {}  # Reset if invalid
        return (valid, msg, self._resume if valid else None)
