# app/api/endpoints/dashboard.py

from fastapi import APIRouter, HTTPException
from app.db.database import SessionLocal
from app.db.models import ProcessedSummary, ProcessedCategory
from app.core.logging import logger

router = APIRouter()

@router.get("/dashboard/summary")
def get_summary():
    logger.info("Fetching summary data for dashboard")
    session = SessionLocal()
    
    try:
        summaries = session.query(ProcessedSummary).all()
        if not summaries:
            logger.warning("No summary data found in the database")
        else:
            logger.info(f"Found {len(summaries)} summary records")
        
        result = [{"description": s.description, "sum_net_amount": s.sum_net_amount} for s in summaries]
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error fetching summary data: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching summary data")
    finally:
        session.close()

@router.get("/dashboard/categorized")
def get_categorized_data():
    logger.info("Fetching categorized data for dashboard")
    session = SessionLocal()
    
    try:
        categories = session.query(ProcessedCategory).all()
        if not categories:
            logger.warning("No categorized data found in the database")
        else:
            logger.info(f"Found {len(categories)} categorized records")
        
        result = [{"order_id": c.order_id, "category": c.category, "details": c.details} for c in categories]
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error fetching categorized data: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching categorized data")
    finally:
        session.close()
