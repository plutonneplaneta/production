from sqlalchemy import Column, Integer, String, Date, Enum, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..models.base import Base


class ProductionOrder(Base):
    __tablename__ = 'ProductionOrders'

    order_id = Column(Integer, primary_key=True)
    order_number = Column(String(50), unique=True, nullable=False)
    start_date = Column(Date, nullable=False)
    planned_end_date = Column(Date)
    actual_end_date = Column(Date)
    status = Column(Enum('open', 'closed'), default='open')
    responsible_person_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    description = Column(Text)

    # Связи
    responsible_user = relationship("User", foreign_keys=[responsible_person_id])