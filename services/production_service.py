# services/production_service.py

from repositories import get_all_production_orders, get_production_order_by_id, create_production_order


def list_all_production_orders():
    return get_all_production_orders()


def get_production_order(order_id: int):
    return get_production_order_by_id(order_id)


def start_production_order(order_number: str, start_date: str, planned_end_date: str = None,
                           actual_end_date: str = None, status: str = 'open',
                           responsible_person_id: int = None, description: str = None):
    return create_production_order(
        order_number=order_number,
        start_date=start_date,
        planned_end_date=planned_end_date,
        actual_end_date=actual_end_date,
        status=status,
        responsible_person_id=responsible_person_id,
        description=description
    )