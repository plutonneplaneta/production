from config.database import SessionLocal
from extra.transfer_order_item import TransferOrderItem


def get_items_by_order(order_id: int):
    db = SessionLocal()
    try:
        return db.query(TransferOrderItem).filter(TransferOrderItem.order_id == order_id).all()
    finally:
        db.close()


def create_transfer_order_item(
    order_id: int,
    material_id: int,
    quantity: float,
    shipped_quantity: float = 0,
    received_quantity: float = 0,
    loss_quantity: float = 0
):
    db = SessionLocal()
    try:
        item = TransferOrderItem(
            order_id=order_id,
            material_id=material_id,
            quantity=quantity,
            shipped_quantity=shipped_quantity,
            received_quantity=received_quantity,
            loss_quantity=loss_quantity
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()