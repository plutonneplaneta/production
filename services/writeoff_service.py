# services/writeoff_service.py

from repositories import get_all_writeoffs, create_writeoff, get_writeoff_items, create_writeoff_item


def list_all_writeoffs():
    return get_all_writeoffs()


def create_new_writeoff(document_number: str, production_order_id: int, warehouse_id: int,
                        writeoff_date: str, written_by: int, status: str = "draft"):
    return create_writeoff(
        document_number=document_number,
        production_order_id=production_order_id,
        warehouse_id=warehouse_id,
        writeoff_date=writeoff_date,
        written_by=written_by,
        status=status
    )


def add_writeoff_item(writeoff_id: int, material_id: int, quantity: float, production_stage: str = None):
    return create_writeoff_item(writeoff_id, material_id, quantity, production_stage)