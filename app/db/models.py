from sqlalchemy import Column, Integer, String, Float, Date, DateTime
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


class ProcessedMTR(Base):
    __tablename__ = "processed_mtr"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, index=True)
    transaction_type = Column(String)
    invoice_date = Column(Date)
    shipment_date = Column(Date)
    order_date = Column(Date)
    shipment_item = Column(String)
    item_description = Column(String)
    invoice_amount = Column(Float)


class ProcessedPayment(Base):
    __tablename__ = "processed_payment"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, index=True)
    date_time = Column(DateTime)
    payment_type = Column(String)
    p_description = Column(String)
    total = Column(Float)
    transaction_type = Column(String, default="Payment")
