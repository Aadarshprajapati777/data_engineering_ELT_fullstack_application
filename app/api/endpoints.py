# app/api/endpoints.py
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.api.elt import perform_elt
from app.core.logging import logger
from app.services.validation import validate_file_extension

router = APIRouter()

@router.get("/health")
async def health_check():
    return JSONResponse(status_code=200, content={"message": "API is healthy"})

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    processed_files = []
    count = 0
    for file in files:
        try:
            logger.info(f"Received file for processing: {file.filename}")
            validate_file_extension(file.filename)
            data = await perform_elt(file)
            processed_files.append(file.filename)
            logger.info(f"ELT process completed successfully for file: {file.filename}")
            logger.info(data)   
            count = count + 1
            logger.info(f"count: {count}")         

        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing file {file.filename}: {str(e)}")

    return {"message": f"Successfully processed files: {processed_files}" }