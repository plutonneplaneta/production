from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .user import User


class TransferOrder(Base):
    __tablename__ = 'TransferOrders'

    order_id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey('TransferRoutes.route_id'))
    shipment_date = Column(Date)
    arrival_date = Column(Date)
    status = Column(Enum('created', 'in_progress', 'completed', 'cancelled'), default='created')
    created_by = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Связи
    filling = relationship("OrderFilling", back_populates="order")
    creator = relationship("User", back_populates="created_order")
    route = relationship("TransferRoute", back_populates="route_order")
    order_loss = relationship("TransferLoss", back_populates="order")
