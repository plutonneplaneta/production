# repositories/output_repository.py

from config.database import SessionLocal
from extra.output import Output


def get_all_outputs():
    db = SessionLocal()
    try:
        return db.query(Output).all()
    finally:
        db.close()


def create_output(
    document_number: str,
    production_order_id: int,
    output_date: str,
    registered_by: int,
    status: str = "draft"
):
    db = SessionLocal()
    try:
        output = Output(
            document_number=document_number,
            production_order_id=production_order_id,
            output_date=output_date,
            registered_by=registered_by,
            status=status
        )
        db.add(output)
        db.commit()
        db.refresh(output)
        return output
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()