from config.database import SessionLocal
from models.material import Material
from models.order_fill import OrderFilling


def get_all_materials():
    db = SessionLocal()
    try:
        return db.query(Material).all()
    finally:
        db.close()


def get_material_by_id(material_id: int):
    db = SessionLocal()
    try:
        return db.query(Material).get(material_id)
    finally:
        db.close()

def get_materials_by_order_id(order_id: int):
    """
    Возвращает список материалов в заказе: (material_id, quantity)
    """
    db = SessionLocal()
    try:
        print(f"Получаем материалы для заказа #{order_id}, тип order_id: {type(order_id)}")
        # Запрашиваем материалы по order_id
        fillings = db.query(OrderFilling).filter(OrderFilling.order_id == order_id).all()

        if not fillings:
            print(f"Нет материалов для заказа #{order_id}")
            return []

        # Возвращаем список кортежей (material_id, quantity)
        return [(filling.material_id, filling.quantity) for filling in fillings]
    except Exception as e:
        print(f"Ошибка при получении материалов: {e}")
        return []
    finally:
        db.close()


def create_material(code: str, name: str, type: str, unit: str,
                    min_stock_level: float = None, max_stock_level: float = None, description: str = None):
    db = SessionLocal()
    try:
        material = Material(
            code=code,
            name=name,
            type=type,
            unit=unit,
            min_stock_level=min_stock_level,
            max_stock_level=max_stock_level,
            description=description
        )
        db.add(material)
        db.commit()
        db.refresh(material)
        return material
    except Exception as e:
        db.rollback()
        print(f"Ошибка при создании материала: {e}")
        raise e
    finally:
        db.close()

def delete_material(name: str):
    db = SessionLocal()
    try:
        material = db.query(Material).filter(Material.name == name).first()
        if material:
            db.delete(material)
            db.commit()
            return True
        else:
            return False
    except Exception as e:
        db.rollback()
        print(f"Ошибка при удалении материала: {e}")
        raise e
    finally:
        db.close()