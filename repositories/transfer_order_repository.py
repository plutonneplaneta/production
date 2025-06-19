from config.database import SessionLocal
from models.transfer_order import TransferOrder
from datetime import datetime


def get_all_transfer_orders():
    db = SessionLocal()
    try:
        return db.query(TransferOrder).all()
    finally:
        db.close()


def get_transfer_order_by_id(order_id: int):
    db = SessionLocal()
    try:
        return db.query(TransferOrder).get(order_id)
    finally:
        db.close()


def create_transfer_order(
    db,
    route_id: int = None,
    status: str = 'created',
    created_at: str = datetime,
    created_by: int = None
) -> int:  # Указываем, что возвращаем int (ID заказа)
    db = SessionLocal()
    try:
        order = TransferOrder(
            route_id=route_id,
            status=status,
            created_at=created_at,
            created_by=created_by
        )
        db.add(order)
        db.flush()

        order_id = order.order_id
        db.commit()
        db.refresh(order)
        return order.order_id  # Возвращаем только ID вместо всего объекта
    except Exception as e:
        db.rollback()
        print(f"Ошибка при создании заказа перемещения: {e}")
        raise e
    finally:
        db.close()

def delete_transfer_order(number: str):
    db = SessionLocal()
    try:
        order = db.query(TransferOrder).filter(TransferOrder.order_number == number).first()
        if order:
            db.delete(order)
            db.commit()
            return True
        else:
            return False
    except Exception as e:
        db.rollback()
        print(f"Ошибка при удалении заказа перемещения: {e}")
        raise e
    finally:
        db.close()

def update_transfer_order(
    order_number: str,
    status: str,
    created_by: int = None
):
    db = SessionLocal()
    try:
        order = TransferOrder(
            order_number=order_number,
            status=status,
            created_by=created_by
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        print(f"Ошибка при изменении заказа перемещения: {e}")
        raise e
    finally:
        db.close()


def update_shipment_data(order_id: int):
    db = SessionLocal()
    try:
        order = db.query(TransferOrder).filter(TransferOrder.order_id == order_id).first()
        if not order:
            raise ValueError(f"Заказ {order_id} не найден")

        if order.status != 'created':
            raise ValueError(f"Невозможно отправить заказ — статус: {order.status}")

        order.shipment_date = datetime.now()
        order.status = 'in_progress'
        db.commit()
        db.refresh(order)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def cancel_shipment(order_id: int):
    db = SessionLocal()
    try:
        order = db.query(TransferOrder).filter(TransferOrder.order_id == order_id).first()
        if not order:
            raise ValueError(f"Заказ {order_id} не найден")

        order.status = 'cancelled'
        db.commit()
        db.refresh(order)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def receive_shipment(order_id: int):
    db = SessionLocal()
    try:
        order = db.query(TransferOrder).filter(TransferOrder.order_id == order_id).first()
        if not order:
            raise ValueError(f"Заказ {order_id} не найден")

        if order.status != "in_progress":
            raise ValueError(f"Невозможно принять заказ — статус: {order.status}")


        order.arrival_date = datetime.now()
        order.status = 'completed'
        db.commit()
        db.refresh(order)
    except Exception as e:
        raise e
    finally:
        db.close()

