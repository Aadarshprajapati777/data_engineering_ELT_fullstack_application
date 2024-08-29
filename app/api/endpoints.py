# app/api/endpoints.py
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.api.elt import perform_elt
from app.core.logging import logger
from app.services.validation import validate_file_extension
# from app.services.elt import perform_elt
# from app.core.logging import logger

# router = APIRouter()

# @router.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     logger.info("Received file for processing")
#     try:
#         data = await perform_elt(file)
#         logger.info("ELT process completed successfully")
#         return {"message": "ELT process completed", "data": data}
#     except Exception as e:
#         logger.error(f"Error during ELT process: {str(e)}")
        # raise HTTPException(status_code=500, detail=str(e))


router = APIRouter()

@router.get("/health")
async def health_check():
    return JSONResponse(status_code=200, content={"message": "API is healthy"})

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    processed_files = []
    for file in files:
        try:
            logger.info(f"Received file for processing: {file.filename}")
            validate_file_extension(file.filename)

            data = await perform_elt(file)
            processed_files.append(file.filename)
            logger.info(f"ELT process completed successfully for file: {file.filename}")
            logger.info(data)            

        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing file {file.filename}: {str(e)}")

    return {"message": f"Successfully processed files: {processed_files}" }