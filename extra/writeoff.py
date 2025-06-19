from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..models.base import Base

class WriteOff(Base):
    __tablename__ = 'ProductionWriteOffs'

    writeoff_id = Column(Integer, primary_key=True)
    document_number = Column(String(50), unique=True, nullable=False)
    production_order_id = Column(Integer, ForeignKey('ProductionOrders.order_id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('Warehouses.warehouse_id'), nullable=False)
    writeoff_date = Column(Date, nullable=False)
    written_by_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    status = Column(Enum('draft', 'confirmed', 'cancelled'), default='draft')
    created_at = Column(TIMESTAMP)

    production_order = relationship("ProductionOrder")
    warehouse = relationship("Warehouse")
    writer = relationship("User")
    items = relationship("WriteOffItem", back_populates="writeoff")