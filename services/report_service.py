
from services.route_service import calculate_route_losses
from repositories import (
    get_all_materials,
    get_all_warehouses,
    get_warehouse_by_id,
    get_stock_balance_by_warehouse_and_material,
    get_all_transfer_orders,
    get_all_transfer_routes,
)


def generate_stock_report(warehouse_id: int = None):
    """
    Сформировать отчёт по остаткам материалов на складе
    Если warehouse_id не указан — по всем складам
    """
    materials = get_all_materials()
    warehouses = get_all_warehouses() if warehouse_id is None else [get_warehouse_by_id(warehouse_id)]

    report_lines = []

    report_lines.append("=== Отчёт по остаткам материалов ===\n")
    for material in materials:
        report_lines.append(f"Материал: {material.name} ({material.code})")
        report_lines.append(f"Единица измерения: {material.unit}")

        has_balance = False
        for warehouse in warehouses:
            balance = get_stock_balance_by_warehouse_and_material(warehouse.warehouse_id, material.material_id)
            if balance:
                report_lines.append(f"  Склад: {warehouse.name} — {balance.quantity}")
                has_balance = True

        if has_balance:
            report_lines.append("")
        else:
            report_lines.append("  Остатков нет\n")

    return report_lines


def generate_transfer_report():
    """
    Отчёт по перемещениям
    """
    orders = get_all_transfer_orders()

    report_lines = []
    report_lines.append("=== Отчёт по перемещениям ===\n")

    for order in orders:
        report_lines.append(f"Номер заказа: {order.order_number}")
        report_lines.append(f"Отправка: {order.from_warehouse.name} → Получение: {order.to_warehouse.name}")
        report_lines.append(f"Статус: {order.status}")
        report_lines.append(f"Количество позиций: {len(order.items)}")
        total_quantity = sum(item.quantity for item in order.items)
        report_lines.append(f"Общее количество: {total_quantity}")
        report_lines.append(f"Создано пользователем: {order.created_by.full_name}")
        report_lines.append("-" * 40)

    return report_lines

def generate_route_reliability_report():
    routes = get_all_transfer_routes()
    report_lines = ["=== Отчёт по надёжности маршрутов ===", ""]

    for route in routes:
        stats = calculate_route_losses(route.route_id)
        if stats:
            report_lines.append(f"Маршрут {route.from_warehouse.name} → {route.to_warehouse.name}")
            report_lines.append(f"Средние потери: {stats['avg_loss']:.2f}%")
            report_lines.append(f"Надёжность: {route.reliability_rating}/10")
            report_lines.append("-" * 40)

    return report_lines

import os

def save_order_document(order_id: int, doc_type: str, content: str):
    folder = os.path.join("reports", "orders", f"ORDER_{order_id}")
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"{doc_type}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def generate_order_content(order, materials):
    lines = [
        f"Документ: Заказ #{order.order_id}",
        f"Дата создания: {order.created_at}",
        f"Статус: {order.status}",
        f"Маршрут: {order.route_id}",
        "Материалы:"
    ]
    for m in materials:
        lines.append(f"  - ID: {m[0]}, Кол-во: {m[1]}")
    return "\n".join(lines)

def generate_shipment_content(order):
    return f"Документ: Отправка заказа #{order.order_id}\nДата отправки: {order.shipment_date}\nСтатус: {order.status}"

def generate_receipt_content(order):
    return f"Документ: Приёмка заказа #{order.order_id}\nДата приёмки: {order.arrival_date}\nСтатус: {order.status}"