from config.database import SessionLocal
from models.order_fill import OrderFilling

def get_fill_order(order_id: str):
    db = SessionLocal()
    try:
        return db.query(OrderFilling).filter(OrderFilling.order_id == order_id).all()
    finally:
        db.close()

def create_filling(
    db,
    order_id: int = None,
    material_id: int = None,
    quantity: int = None
):
    db = SessionLocal()
    try:
        filling = OrderFilling(
            order_id=order_id,
            material_id=material_id,
            quantity=quantity
        )
        db.add(filling)
        db.commit()
        db.refresh(filling)
        return filling
    except Exception as e:
        db.rollback()
        print(f"Ошибка: {e}")
        raise e
    finally:
        db.close()

def delete_order(order_id: str):
    db = SessionLocal()
    try:
        order = db.query(OrderFilling).filter(OrderFilling.order_id == order_id).all()
        if order:
            db.delete(order)
            db.commit()
            return True
        else:
            return False
    except Exception as e:
        db.rollback()
        print(f"Ошибка удаления: {e}")
        raise e
    finally:
        db.close()