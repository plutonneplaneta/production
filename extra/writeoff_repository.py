# repositories/writeoff_repository.py

from config.database import SessionLocal
from writeoff import WriteOff


def get_all_writeoffs():
    db = SessionLocal()
    try:
        return db.query(WriteOff).all()
    finally:
        db.close()


def create_writeoff(
    document_number: str,
    production_order_id: int,
    warehouse_id: int,
    writeoff_date: str,
    written_by: int,
    status: str = "draft"
):
    db = SessionLocal()
    try:
        writeoff = WriteOff(
            document_number=document_number,
            production_order_id=production_order_id,
            warehouse_id=warehouse_id,
            writeoff_date=writeoff_date,
            written_by=written_by,
            status=status
        )
        db.add(writeoff)
        db.commit()
        db.refresh(writeoff)
        return writeoff
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()