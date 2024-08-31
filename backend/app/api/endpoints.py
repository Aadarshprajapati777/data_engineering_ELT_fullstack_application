from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.api.elt import perform_elt
from app.core.logging import logger
from app.services.validation import validate_file_extension

router = APIRouter()

@router.get("/health")
async def health_check():
    logger.info("Health check endpoint hit")
    return JSONResponse(status_code=200, content={"message": "API is healthy"})

@router.post("/upload")
async def upload_files(mtr_file: UploadFile = File(...), payment_file: UploadFile = File(...)):
    logger.info("Upload endpoint hit")

    try:
        logger.info(f"Validating file extensions")
        validate_file_extension(mtr_file.filename)
        validate_file_extension(payment_file.filename)

        logger.info(f"Processing files: {mtr_file.filename} and {payment_file.filename}")
        
        data = await perform_elt(mtr_file, payment_file)
        logger.info(f"ELT process completed successfully for files: {mtr_file.filename} and {payment_file.filename}")
        return {"message": "Successfully processed MTR and Payment files."}
    except Exception as e:
        logger.error(f"Error during ELT process: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during ELT process: {str(e)}")
