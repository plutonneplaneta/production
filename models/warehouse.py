from sqlalchemy import Column, Integer, String, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class Warehouse(Base):
    __tablename__ = 'Warehouses'

    warehouse_id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    type = Column(Enum('production', 'transit', 'finished_products'), nullable=False)
    location = Column(String(255))
    is_active = Column(Boolean, default=True)
    description = Column(Text)

    stock_items = relationship("StockBalance", back_populates="warehouse")

    # TransferRoute: связи по типам складов
    shipping_routes = relationship("TransferRoute", foreign_keys='[TransferRoute.from_warehouse_id]', back_populates="from_warehouse")
    receiving_routes = relationship("TransferRoute", foreign_keys='[TransferRoute.to_warehouse_id]', back_populates="to_warehouse")
    transit_routes = relationship("TransferRoute", foreign_keys='[TransferRoute.transit_warehouse_id]', back_populates="transit_warehouse")
    # Другие связи
    shipments = relationship("Shipment", back_populates="warehouse")  # Склад отгрузки
    receipts = relationship("Receipt", back_populates="to_warehouse")  # Склад приёмки