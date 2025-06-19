# services/transfer_service.py

from repositories import get_all_transfer_routes, get_transfer_route_by_id, create_transfer_route
from repositories import get_all_transfer_orders, get_transfer_order_by_id, create_transfer_order


def list_all_transfer_routes():
    return get_all_transfer_routes()


def get_transfer_route(route_id: int):
    return get_transfer_route_by_id(route_id)


def create_new_transfer_route(from_warehouse_id: int, to_warehouse_id: int, transit_warehouse_id: int = None,
                              transport_method: str = None, duration_hours: int = None):
    return create_transfer_route(
        from_warehouse_id=from_warehouse_id,
        to_warehouse_id=to_warehouse_id,
        transit_warehouse_id=transit_warehouse_id,
        transport_method=transport_method,
        duration_hours=duration_hours
    )


def list_all_transfer_orders():
    return get_all_transfer_orders()


def get_transfer_order(order_id: int):
    return get_transfer_order_by_id(order_id)


def create_new_transfer_order(
    order_number: str,
    from_warehouse_id: int,
    to_warehouse_id: int,
    transit_warehouse_id: int = None,
    route_id: int = None,
    planned_shipment_date: str = None,
    planned_arrival_date: str = None,
    status: str = 'created',
    created_by: int = None
):
    return create_transfer_order(
        order_number=order_number,
        from_warehouse_id=from_warehouse_id,
        to_warehouse_id=to_warehouse_id,
        transit_warehouse_id=transit_warehouse_id,
        route_id=route_id,
        planned_shipment_date=planned_shipment_date,
        planned_arrival_date=planned_arrival_date,
        status=status,
        created_by=created_by
    )