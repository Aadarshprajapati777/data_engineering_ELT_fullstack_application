# app/services/load.py
from sqlalchemy.orm import Session
from app.db.models import ProcessedData
from app.db.database import SessionLocal
from app.core.logging import logger

def load_data(datasets: dict):
    db: Session = SessionLocal()
    try:
        for dataset_name, df in datasets.items():
            for _, row in df.iterrows():
                db_data = ProcessedData(dataset=dataset_name, **row.to_dict())
                db.add(db_data)
        db.commit()
        logger.info("Data successfully loaded to the database")
    except Exception as e:
        logger.error(f"Failed to load data: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()
