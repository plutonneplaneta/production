# repositories/transfer_history_repository.py

from config.database import SessionLocal
from extra.transfer_history import TransferHistory


def log_transfer(
    order_id: int,
    material_id: int,
    from_warehouse_id: int,
    to_warehouse_id: int,
    quantity: float,
    transaction_type: str,
    document_id: int = None,
    document_type_id: int = None,
    user_id: int = None
):
    db = SessionLocal()
    try:
        history = TransferHistory(
            order_id=order_id,
            material_id=material_id,
            from_warehouse_id=from_warehouse_id,
            to_warehouse_id=to_warehouse_id,
            quantity=quantity,
            transaction_type=transaction_type,
            document_id=document_id,
            document_type_id=document_type_id,
            user_id=user_id
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()