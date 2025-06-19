from sqlalchemy import Column, Integer, DECIMAL, TIMESTAMP,ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class StockBalance(Base):
    __tablename__ = 'StockBalances'

    balance_id = Column(Integer, primary_key=True)
    warehouse_id = Column(Integer, ForeignKey('Warehouses.warehouse_id'), nullable=False)
    material_id = Column(Integer, ForeignKey('Materials.material_id'), nullable=False)
    quantity = Column(DECIMAL(precision=12, scale=3), nullable=False)
    last_update = Column(TIMESTAMP)

    warehouse = relationship("Warehouse", back_populates="stock_items")
    material = relationship("Material", back_populates="stock_items")