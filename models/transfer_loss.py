from sqlalchemy import Column, Integer, DECIMAL, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import Base

class TransferLoss(Base):
    __tablename__ = 'TransferLosses'

    loss_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('TransferOrders.order_id'), nullable=False)
    route_id = Column(Integer, ForeignKey('TransferRoutes.route_id'), nullable=False)
    material_id = Column(Integer, ForeignKey('Materials.material_id'), nullable=False)
    expected_quantity = Column(DECIMAL(12, 3), nullable=False)
    actual_quantity = Column(DECIMAL(12, 3), nullable=False)
    loss_percentage = Column(DECIMAL(5, 2))  # генерируется автоматически в БД
    loss_reason = Column(String(255))
    recorded_date = Column(Date, nullable=False)
    recorded_by_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)

    recorded_by = relationship("User", back_populates="recorded_loss")
    material = relationship("Material", back_populates="losses")
    route = relationship("TransferRoute", back_populates="route_loss")
    order = relationship("TransferOrder", back_populates="order_loss")