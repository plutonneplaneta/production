# repositories/stock_balance_repository.py

from config.database import SessionLocal
from models.stock_balance import StockBalance


def get_stock_balance_by_warehouse_and_material(warehouse_id: int, material_id: int):
    db = SessionLocal()
    try:
        return db.query(StockBalance).filter(
            StockBalance.warehouse_id == warehouse_id,
            StockBalance.material_id == material_id
        ).first()
    finally:
        db.close()


def update_or_create_stock_balance(db,warehouse_id: int, material_id: int, quantity: float):
    #db = SessionLocal()
    try:
        balance = get_stock_balance_by_warehouse_and_material(warehouse_id, material_id)
        if balance:
            balance.quantity = quantity
        else:
            balance = StockBalance(
                warehouse_id=warehouse_id,
                material_id=material_id,
                quantity=quantity
            )
            db.add(balance)
        #db.commit()
        #db.refresh(balance)
        db.flush()
        return balance
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def subtract_material_from_warehouse(warehouse_id: int, material_id: int, quantity_to_subtract: float):
    """
    Вычитает количество материала из остатка на складе
    """
    db = SessionLocal()
    from models.stock_balance import StockBalance
    from decimal import Decimal
    from datetime import datetime

    balance = db.query(StockBalance).filter(
        StockBalance.warehouse_id == warehouse_id,
        StockBalance.material_id == material_id
    ).first()

    if not balance:
        raise ValueError(f"Нет остатка для материала #{material_id} на складе #{warehouse_id}")

    if balance.quantity < quantity_to_subtract:
        raise ValueError(f"На складе #{warehouse_id} недостаточно {balance.material.name}")
    print(f"warehouse_id {balance.warehouse_id}")
    print(f"quantity_to_subtract {quantity_to_subtract}")
    print(f"balance.quantity {balance.quantity}")
    print(f"balance.last_update {balance.last_update}")
    # Вычитаем
    balance.quantity -= Decimal(str(quantity_to_subtract))
    balance.last_update = datetime.now()
    db.add(balance)
    print(f"balance.last_update после вычитания {balance.last_update}")
    db.commit()