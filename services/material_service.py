# services/material_service.py

from repositories import get_all_materials, get_material_by_id, create_material


def list_all_materials():
    return get_all_materials()


def get_material(material_id: int):
    return get_material_by_id(material_id)


def add_material(code: str, name: str, type: str, unit: str,
                 min_stock_level: float = None, max_stock_level: float = None, description: str = None):
    return create_material(code, name, type, unit, min_stock_level, max_stock_level, description)