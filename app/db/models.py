from sqlalchemy import Column, Integer, String, Float, Date
from app.db.database import Base

class MergedData(Base):
    __tablename__ = "merged_data"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, index=True)
    transaction_type = Column(String)
    payment_type = Column(String)
    invoice_amount = Column(Float)
    net_amount = Column(Float)
    p_description = Column(String)
    order_date = Column(Date)
    payment_date = Column(Date)
