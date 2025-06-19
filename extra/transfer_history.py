# models/transfer_history.py
from sqlalchemy import Column, Integer, DECIMAL, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..models.base import Base

class TransferHistory(Base):
    __tablename__ = 'TransferHistory'

    history_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('TransferOrders.order_id'), nullable=False)
    material_id = Column(Integer, ForeignKey('Materials.material_id'), nullable=False)
    from_warehouse_id = Column(Integer, ForeignKey('Warehouses.warehouse_id'), nullable=False)
    to_warehouse_id = Column(Integer, ForeignKey('Warehouses.warehouse_id'), nullable=False)
    quantity = Column(DECIMAL(12, 3))
    transaction_date = Column(TIMESTAMP)
    transaction_type = Column(Enum('shipment', 'receipt', 'writeoff', 'production_output'), nullable=False)
    document_id = Column(Integer)
    document_type_id = Column(Integer, ForeignKey('DocumentTypes.type_id'))
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)

    transfer_order = relationship("TransferOrder")
    material = relationship("Material")
    from_warehouse = relationship("Warehouse", foreign_keys=[from_warehouse_id])
    to_warehouse = relationship("Warehouse", foreign_keys=[to_warehouse_id])
    user = relationship("User")
    document_type = relationship("DocumentType")