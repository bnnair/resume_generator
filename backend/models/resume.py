
from pydantic import BaseModel, field_validator
from typing import List, Optional

class PersonalDetails(BaseModel):
    name: str
    location: str
    country: str
    mobile: str
    email: str
    github: str
    linkedin: str

class Summary (BaseModel):
    summary: str

class Experience(BaseModel):
    company: str
    position: str
    duration: str
    responsibilities: Optional[List[str]] = None

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    duration: str

class Achievement(BaseModel):
    name: str
    description : str

class Skill(BaseModel):
    name: str
    description : str

class Certification(BaseModel):
    name: str
    description: str
    
class Resume(BaseModel):
    personalDetails: PersonalDetails
    summary: Summary
    experiences: List[Experience]
    education: List[Education]
    achievements: Optional[List[Achievement]] = None
    skills: List[Skill]
    certifications: Optional[List[Certification]] = None