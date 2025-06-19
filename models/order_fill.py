from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .user import User


class OrderFilling(Base):
    __tablename__ = 'OrderFilling'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('TransferOrders.order_id'))
    material_id = Column(Integer, ForeignKey('Materials.material_id'))
    quantity = Column(DECIMAL(12, 3), nullable=False)
    # Связи
    order = relationship("TransferOrder", back_populates="filling")
    material = relationship("Material", back_populates="order")

    
 