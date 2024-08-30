import os
from fastapi import HTTPException
from app.core.logging import logger
from app.core.config import valid_extensions

def validate_file_extension(filename: str):
    logger.info(f"Validating file extension for file: {filename}")
    
    ext = os.path.splitext(filename)[1].lower()  
    
    if ext not in valid_extensions:
        logger.error(f"Invalid file extension: {ext}")
        raise HTTPException(status_code=400, detail="Invalid file extension")
    
    logger.info(f"File extension validated: {ext}")
