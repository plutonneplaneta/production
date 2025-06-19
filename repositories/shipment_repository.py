# repositories/shipment_repository.py

from config.database import SessionLocal
from models.shipment import Shipment


def get_all_shipments():
    db = SessionLocal()
    try:
        return db.query(Shipment).all()
    finally:
        db.close()


def create_shipment(
    order_id: int,
    document_number: str,
    shipment_date: str,
    shipped_by: int,
    warehouse_id: int,
    status: str = "draft"
):
    db = SessionLocal()
    try:
        shipment = Shipment(
            order_id=order_id,
            document_number=document_number,
            shipment_date=shipment_date,
            shipped_by=shipped_by,
            warehouse_id=warehouse_id,
            status=status
        )
        db.add(shipment)
        db.commit()
        db.refresh(shipment)
        return shipment
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()