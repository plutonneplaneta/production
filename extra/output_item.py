from sqlalchemy import Column, Integer, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..models.base import Base

class OutputItem(Base):
    __tablename__ = 'ProductionOutputItems'

    item_id = Column(Integer, primary_key=True)
    output_id = Column(Integer, ForeignKey('ProductionOutputs.output_id'), nullable=False)
    material_id = Column(Integer, ForeignKey('Materials.material_id'), nullable=False)
    quantity = Column(DECIMAL(12, 3), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('Warehouses.warehouse_id'))
    is_semi_finished = Column(Boolean, default=False)

    output = relationship("Output", back_populates="items")
    material = relationship("Material")
    warehouse = relationship("Warehouse")