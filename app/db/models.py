from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class MergedData(Base):
    __tablename__ = "merged_data"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, index=True)
    transaction_type = Column(String)
    payment_type = Column(String)
    net_amount = Column(Float)
    invoice_amount = Column(Float)
    payment_net_amount = Column(Float)
    shipment_invoice_amount = Column(Float)
    # Additional fields based on your dataset

class TransformedData(Base):
    __tablename__ = "transformed_data"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset = Column(String, index=True)
    order_id = Column(String, index=True)
    transaction_type = Column(String)
    payment_type = Column(String)
    net_amount = Column(Float)
    invoice_amount = Column(Float)
    # Additional fields as needed
