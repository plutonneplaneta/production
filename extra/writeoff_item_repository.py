# repositories/writeoff_item_repository.py

from config.database import SessionLocal
from writeoff_item import WriteOffItem


def get_writeoff_items(writeoff_id: int):
    db = SessionLocal()
    try:
        return db.query(WriteOffItem).filter(WriteOffItem.writeoff_id == writeoff_id).all()
    finally:
        db.close()


def create_writeoff_item(
    writeoff_id: int,
    material_id: int,
    quantity: float,
    production_stage: str = None
):
    db = SessionLocal()
    try:
        item = WriteOffItem(
            writeoff_id=writeoff_id,
            material_id=material_id,
            quantity=quantity,
            production_stage=production_stage
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