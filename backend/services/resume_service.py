# backend/main.py
import os
import tempfile
from logging_config import logger
from dotenv import load_dotenv

from fastapi import File, HTTPException, status
from utils.config_manager import ConfigManager
from utils.pdf_parser import load_pdf

from models.resume import Resume

from services.llm_manager import AIAdapter

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate



class ResumeService:
    """Handles resume processing and data extraction."""
    
    async def upload_resume(self, file: File):
        """
        Upload a PDF resume and get back an enhanced version
        """
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed"
            )
        try:
            MODEL_TYPE = "openai"
            # Call the LLM to enhance the resume
            config = ConfigManager.update_config()
            logger.debug(f"config : {config}")
            aiadapter = AIAdapter(config, MODEL_TYPE)
            logger.debug(f"adapter : {aiadapter}")

            # Save the uploaded file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(await file.read())
                temp_file_path = temp_file.name

            pages = load_pdf(temp_file_path)
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
            parser = JsonOutputParser(pydantic_object=Resume)

            prompt = PromptTemplate(
            template="Extract the information as specified.  \
                do not extract any other information other than the specified\n{format_instructions}\n{context}\n",
            input_variables=["context"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
            )
            
            logger.info("calling aiadapter invoke method")
            response = aiadapter.invoke(prompt.format(context=pages))
            response1 = parser.invoke(response)
            
            logger.info(f"completed Response------>{response1}")
            return response1      
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing resume: {str(e)}"
            )