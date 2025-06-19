from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum("admin", "warehouse_manager", "production_manager", "logistics"), nullable=False)
    is_active = Column(Boolean, default=True)
    last_login = Column(TIMESTAMP)

    created_order = relationship("TransferOrder", back_populates="creator")
    recorded_loss = relationship("TransferLoss", back_populates="recorded_by")
    created_shipment = relationship("Shipment", back_populates="shipped_by")
    created_receipt = relationship("Receipt", back_populates="received_by") 