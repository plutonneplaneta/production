from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey
from sqlalchemy.orm import relationship
from ..models.base import Base

class WriteOffItem(Base):
    __tablename__ = 'ProductionWriteOffItems'

    item_id = Column(Integer, primary_key=True)
    writeoff_id = Column(Integer, ForeignKey('ProductionWriteOffs.writeoff_id'), nullable=False)
    material_id = Column(Integer, ForeignKey('Materials.material_id'), nullable=False)
    quantity = Column(DECIMAL(12, 3), nullable=False)
    production_stage = Column(String(255))

    writeoff = relationship("WriteOff", back_populates="items")
    material = relationship("Material")