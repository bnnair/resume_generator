from pydantic import BaseModel
from typing import  Optional, List

class JobDescriptionModel(BaseModel):
    company: str
    jobTitle: str
    jobLink: Optional[str]=None
    jobLocation: str
    resumeGenerated:bool
    jobDesc: str

class JDList(BaseModel):
    jobDescription: List[JobDescriptionModel]