from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from ..models.base import Base

class TransferOrderItem(Base):
    __tablename__ = 'TransferOrderItems'

    item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('TransferOrders.order_id'), nullable=False)
    material_id = Column(Integer, ForeignKey('Materials.material_id'), nullable=False)
    quantity = Column(DECIMAL(12, 3), nullable=False)
    shipped_quantity = Column(DECIMAL(12, 3), default=0)
    received_quantity = Column(DECIMAL(12, 3), default=0)
    loss_quantity = Column(DECIMAL(12, 3), default=0)

    order = relationship("TransferOrder", back_populates="items")
    material = relationship("Material")