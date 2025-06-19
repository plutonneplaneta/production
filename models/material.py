from sqlalchemy import Column, Integer, String, Enum, DECIMAL, Boolean, Text
from sqlalchemy.orm import relationship
from .base import Base


class Material(Base):
    __tablename__ = 'Materials'

    material_id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(Enum('raw', 'material', 'semi_finished', 'finished'), nullable=False)
    unit = Column(String(20), nullable=False)
    min_stock_level = Column(DECIMAL(precision=12, scale=3))
    max_stock_level = Column(DECIMAL(precision=12, scale=3))
    production_status = Column(Enum('in_progress', 'decommissioned', 'released'), nullable=False)
    description = Column(Text)

    stock_items = relationship("StockBalance", back_populates="material")
    losses = relationship("TransferLoss", back_populates="material")
    order = relationship("OrderFilling", back_populates="material")

    from models.order_fill import OrderFilling