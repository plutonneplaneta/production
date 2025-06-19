from config.database import SessionLocal
from models.warehouse import Warehouse


def get_all_warehouses():
    db = SessionLocal()
    try:
        return db.query(Warehouse).all()
    finally:
        db.close()


def get_warehouse_by_id(warehouse_id: int):
    db = SessionLocal()
    try:
        return db.query(Warehouse).get(warehouse_id)
    finally:
        db.close()

def get_warehouse_name_by_id(warehouse_id:int):
    db = SessionLocal()
    try:
        warehouse = db.query(Warehouse).get(warehouse_id)
        return warehouse.name
    finally:
        db.close()


def create_warehouse(name: str, type: str, location: str = None, description: str = None):
    db = SessionLocal()
    try:
        warehouse = Warehouse(name=name, type=type, location=location, description=description)
        db.add(warehouse)
        db.commit()
        db.refresh(warehouse)
        return warehouse
    except Exception as e:
        db.rollback()
        print(f"Ошибка при создании склада: {e}")
        raise e
    finally:
        db.close()

def update_warehouse(warehouse_id, name, type, location,  is_active):
    db = SessionLocal()
    try:
        warehouse = db.query(Warehouse).filter(Warehouse.warehouse_id == warehouse_id).first()
        if not warehouse:
            raise ValueError(f"Склад с ID {warehouse_id} не найден")

        warehouse.name = name
        warehouse.type = type
        warehouse.location = location
        warehouse.is_active = is_active

        db.commit()
        db.refresh(warehouse)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def delete_warehouse(name: str):
    db = SessionLocal()
    try:
        warehouse = db.query(Warehouse).filter(Warehouse.name == name).first()
        if warehouse:
            db.delete(warehouse)
            db.commit()
            return True
        else:
            return False
    except Exception as e:
        db.rollback()
        print(f"Ошибка при удалении склада: {e}")
        raise e
    finally:
        db.close()