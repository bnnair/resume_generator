# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services.api.resume_api import resume_router
from services.api.jd_api import jd_router

import os
from dotenv import load_dotenv
from logging_config import logger

# Load environment variables
load_dotenv()
app = FastAPI(
    title="AI Resume Generator",
    description="API for resume enhancement and generation",
    version="1.0.0",
)

app.include_router(resume_router)
app.include_router(jd_router)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], ## for production, this should be limited to specific domains
    allow_methods=["*"], ## for production, this should be limited to specific methods
    allow_headers=["*"], ## for production, this should be limited to specific headers
    allow_credentials=True,
)

# Custom exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000))
    )
