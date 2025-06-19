# repositories/production_order_repository.py

from config.database import SessionLocal
from extra.production_order import ProductionOrder


def get_production_order_by_id(order_id: int):
    db = SessionLocal()
    try:
        return db.query(ProductionOrder).filter(ProductionOrder.order_id == order_id).first()
    finally:
        db.close()


def get_all_production_orders():
    db = SessionLocal()
    try:
        return db.query(ProductionOrder).all()
    finally:
        db.close()


def create_production_order(
    order_number: str,
    start_date: str,
    planned_end_date: str = None,
    actual_end_date: str = None,
    status: str = 'open',
    responsible_person_id: int = None,
    description: str = None
):
    db = SessionLocal()
    try:
        new_order = ProductionOrder(
            order_number=order_number,
            start_date=start_date,
            planned_end_date=planned_end_date,
            actual_end_date=actual_end_date,
            status=status,
            responsible_person_id=responsible_person_id,
            description=description
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()