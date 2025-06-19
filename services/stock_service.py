# services/stock_service.py

from repositories import get_stock_balance_by_warehouse_and_material, update_or_create_stock_balance


def get_stock_balance(warehouse_id: int, material_id: int):
    return get_stock_balance_by_warehouse_and_material(warehouse_id, material_id)


def update_stock_balance(warehouse_id: int, material_id: int, quantity: float):
    return update_or_create_stock_balance(warehouse_id, material_id, quantity)


def has_enough_stock(warehouse_id: int, material_id: int, needed_quantity: float):
    balance = get_stock_balance_by_warehouse_and_material(warehouse_id, material_id)
    if balance and balance.quantity >= needed_quantity:
        return True
    return False