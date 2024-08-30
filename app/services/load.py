from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import MergedData
from app.core.logging import logger
import pandas as pd

def load_data_to_db(merged_df: pd.DataFrame):
    logger.info("Loading data into the database")
    
    db: Session = SessionLocal()
    try:
        for _, row in merged_df.iterrows():
            db_record = MergedData(**row.to_dict())
            db.add(db_record)
        
        db.commit()
        logger.info("Data successfully loaded into the database")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error loading data into the database: {str(e)}")
        raise e
    
    finally:
        db.close()
        logger.info("Database session closed")
  