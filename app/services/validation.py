import pandas as pd
from app.core.logging import logger
from app.services.custom_exceptions import FileValidationError

def validate_file_extension(filename: str):
    logger.info("Inside file validation")
    if not (filename.endswith('.csv') or filename.endswith('.xlsx')):
        raise FileValidationError()