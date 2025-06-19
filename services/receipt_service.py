# services/receipt_service.py

from repositories import get_all_receipts, create_receipt


def list_all_receipts():
    return get_all_receipts()


def record_receipt(order_id: int, document_number: str, receipt_date: str,
                   received_by: int, warehouse_id: int, status: str = "draft"):
    return create_receipt(
        order_id=order_id,
        document_number=document_number,
        receipt_date=receipt_date,
        received_by=received_by,
        warehouse_id=warehouse_id,
        status=status
    )