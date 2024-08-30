from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import MergedData, ProcessedMTR, ProcessedPayment
from app.core.logging import logger
import pandas as pd

def load_merged_data_to_db(merged_df: pd.DataFrame):
    logger.info("Loading merged data into the database")
    
    db: Session = SessionLocal()
    try:
        for _, row in merged_df.iterrows():
            db_record = MergedData(**row.to_dict())
            db.add(db_record)
        
        db.commit()
        logger.info("Merged Data successfully loaded into the database")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error loading data into the database: {str(e)}")
        raise e


def load_processed_payment_data_to_db(merged_df: pd.DataFrame):
    logger.info("Loading processed payement data into the database")
    
    db: Session = SessionLocal()
    try:
        for _, row in merged_df.iterrows():
            db_record = ProcessedPayment(**row.to_dict())
            db.add(db_record)
        
        db.commit()
        logger.info("processed payment Data successfully loaded into the database")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error loading data into the database: {str(e)}")
        raise e


def load_processed_mtr_data_to_db(merged_df: pd.DataFrame):
    logger.info("Loading processed mtr data into the database")
    
    db: Session = SessionLocal()
    try:
        for _, row in merged_df.iterrows():
            db_record = ProcessedMTR(**row.to_dict())
            db.add(db_record)
        
        db.commit()
        logger.info("processed mtr Data successfully loaded into the database")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error loading data into the database: {str(e)}")
        raise e

    finally:
        db.close()
        logger.info("Database session closed")
  