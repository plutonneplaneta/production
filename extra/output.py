from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..models.base import Base

class Output(Base):
    __tablename__ = 'ProductionOutputs'

    output_id = Column(Integer, primary_key=True)
    document_number = Column(String(50), unique=True, nullable=False)
    production_order_id = Column(Integer, ForeignKey('ProductionOrders.order_id'), nullable=False)
    output_date = Column(Date, nullable=False)
    registered_by_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    status = Column(Enum('draft', 'confirmed', 'cancelled'), default='draft')
    created_at = Column(TIMESTAMP)

    production_order = relationship("ProductionOrder")
    user = relationship("User")
    items = relationship("OutputItem", back_populates="output")