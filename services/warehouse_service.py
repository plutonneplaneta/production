# services/warehouse_service.py

from repositories import get_all_warehouses, get_warehouse_by_id, create_warehouse
from config.database import SessionLocal
from models.warehouse import Warehouse

def list_all_warehouses():
    return get_all_warehouses()


def get_warehouse(warehouse_id: int):
    return get_warehouse_by_id(warehouse_id)


def add_warehouse(name: str, type: str, location: str = None, description: str = None):
    return create_warehouse(name, type, location, description)

def get_all_warehouses():
    db = SessionLocal()
    try:
        return db.query(Warehouse).all()
    finally:
        db.close()