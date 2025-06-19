from config.database import SessionLocal
from models.transfer_route import TransferRoute
from models.transfer_order import TransferOrder

def get_all_transfer_routes():
    db = SessionLocal()
    try:
        return db.query(TransferRoute).all()
    finally:
        db.close()

def get_transfer_route_by_id(route_id: int):
    db = SessionLocal()
    try:
        return db.query(TransferRoute).get(route_id)
    finally:
        db.close()

def get_transfer_route_by_order_id(order_id: int):
    """
    Возвращает объект TransferRoute, связанный с заказом
    """
    db = SessionLocal()
    try:
        # Находим заказ
        transfer_order = db.query(TransferOrder).get(order_id)
        if not transfer_order:
            raise ValueError(f"Заказ #{order_id} не найден")

        # Получаем маршрут по route_id
        return transfer_order.route # это ORM-объект TransferRoute
    finally:
        db.close()

def create_transfer_route(
    from_warehouse_id: int,
    to_warehouse_id: int,
    transit_warehouse_id: int = None,
    transport_method: str = None,
    duration_hours: int = None,
    reliability_rating: float = 5.00
):
    db = SessionLocal()
    try:
        route = TransferRoute(
            from_warehouse_id=from_warehouse_id,
            to_warehouse_id=to_warehouse_id,
            transit_warehouse_id=transit_warehouse_id,
            transport_method=transport_method,
            duration_hours=duration_hours,
            reliability_rating=reliability_rating
        )
        db.add(route)
        db.commit()
        db.refresh(route)
        return route
    except Exception as e:
        db.rollback()
        print(f"Ошибка при создании маршрута перемещения: {e}")
        raise e
    finally:
        db.close()

def delete_transfer_route(route_id: str):
    db = SessionLocal()
    try:
        route = db.query(TransferRoute).filter(TransferRoute.route_id == route_id).first()
        if route:
            db.delete(route)
            db.commit()
            return True
        else:
            return False
    except Exception as e:
        db.rollback()
        print(f"Ошибка при удалении маршрута перемещения: {e}")
        raise e
    finally:
        db.close()

def update_transfer_route(
    route_id: int,
    reliability_rating: float = 5.00
):
    db = SessionLocal()
    try:
        route = TransferRoute(
            route_id=route_id,
            reliability_rating=reliability_rating
        )
        db.add(route)
        db.commit()
        db.refresh(route)
        return route
    except Exception as e:
        db.rollback()
        print(f"Ошибка при изменении маршрута перемещения: {e}")
        raise e
    finally:
        db.close()

# repositories/transfer_route_repository.py

def update_transfer_route_with_new(route_id: int, data: dict):
    db = SessionLocal()
    try:
        route = db.query(TransferRoute).get(route_id)
        if not route:
            raise ValueError(f"Маршрут #{route_id} не найден")

        for key, value in data.items():
            if hasattr(route, key):
                setattr(route, key, value)

        db.add(route)
        db.commit()
        db.refresh(route)
        return route
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()