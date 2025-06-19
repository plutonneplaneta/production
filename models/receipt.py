from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Receipt(Base):
    __tablename__ = 'Receipts'

    receipt_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('TransferOrders.order_id'), nullable=False)
    document_number = Column(String(50), unique=True, nullable=False)
    receipt_date = Column(Date, nullable=False)
    received_by_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('Warehouses.warehouse_id'), nullable=False)
    status = Column(Enum('draft', 'confirmed', 'cancelled'), default='draft')
    created_at = Column(TIMESTAMP)

    received_by = relationship("User", back_populates="created_receipt")
    to_warehouse = relationship("Warehouse", back_populates="receipts")