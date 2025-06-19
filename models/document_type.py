from sqlalchemy import Column, Integer, Enum, Text
#from sqlalchemy.orm import relationship
from .base import Base

class DocumentType(Base):
    __tablename__ = 'DocumentTypes'

    type_id = Column(Integer, primary_key=True)
    type_name = Column(Enum('create_order', 'shipment', 'receipt', 'production_output'), nullable=False)
    description = Column(Text)
