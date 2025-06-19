# repositories/receipt_repository.py

from config.database import SessionLocal
from models.receipt import Receipt


def get_all_receipts():
    db = SessionLocal()
    try:
        return db.query(Receipt).all()
    finally:
        db.close()


def create_receipt(
    order_id: int,
    document_number: str,
    receipt_date: str,
    received_by: int,
    warehouse_id: int,
    status: str = "draft"
):
    db = SessionLocal()
    try:
        receipt = Receipt(
            order_id=order_id,
            document_number=document_number,
            receipt_date=receipt_date,
            received_by=received_by,
            warehouse_id=warehouse_id,
            status=status
        )
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        return receipt
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()