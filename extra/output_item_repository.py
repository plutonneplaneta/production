# repositories/output_item_repository.py

from config.database import SessionLocal
from extra.output_item import OutputItem


def get_output_items(output_id: int):
    db = SessionLocal()
    try:
        return db.query(OutputItem).filter(OutputItem.output_id == output_id).all()
    finally:
        db.close()


def create_output_item(
    output_id: int,
    material_id: int,
    quantity: float,
    warehouse_id: int = None,
    is_semi_finished: bool = False
):
    db = SessionLocal()
    try:
        item = OutputItem(
            output_id=output_id,
            material_id=material_id,
            quantity=quantity,
            warehouse_id=warehouse_id,
            is_semi_finished=is_semi_finished
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