# services/shipment_service.py

from repositories import get_all_shipments, create_shipment


def list_all_shipments():
    return get_all_shipments()


def record_shipment(order_id: int, document_number: str, shipment_date: str,
                    shipped_by: int, warehouse_id: int, status: str = "draft"):
    return create_shipment(
        order_id=order_id,
        document_number=document_number,
        shipment_date=shipment_date,
        shipped_by=shipped_by,
        warehouse_id=warehouse_id,
        status=status
    )