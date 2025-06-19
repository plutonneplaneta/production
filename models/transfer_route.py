from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class TransferRoute(Base):
    __tablename__ = 'TransferRoutes'

    route_id = Column(Integer, primary_key=True)
    from_warehouse_id = Column(Integer, ForeignKey('Warehouses.warehouse_id'), nullable=False)
    to_warehouse_id = Column(Integer, ForeignKey('Warehouses.warehouse_id'), nullable=False)
    transit_warehouse_id = Column(Integer, ForeignKey('Warehouses.warehouse_id'))
    transport_method = Column(String(50))
    duration_hours = Column(Integer, nullable=False)
    reliability_rating = Column(DECIMAL(3, 2), default=5.00)
    is_active = Column(Boolean, default=True)

    # Связи
    route_loss = relationship("TransferLoss", back_populates="route")
    route_order = relationship("TransferOrder", back_populates="route")

    from_warehouse = relationship("Warehouse", foreign_keys=[from_warehouse_id], back_populates="shipping_routes")
    to_warehouse = relationship("Warehouse", foreign_keys=[to_warehouse_id], back_populates="receiving_routes")
    transit_warehouse = relationship("Warehouse", foreign_keys=[transit_warehouse_id], back_populates="transit_routes")