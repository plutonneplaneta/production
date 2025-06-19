# services/route_service.py

from repositories import get_all_transfer_routes, report_transfer_loss
from repositories import get_all_transfer_orders

def find_best_routes(from_warehouse_id: int, to_warehouse_id: int):
    routes = get_all_transfer_routes()
    suitable_routes = [
        r for r in routes
        if r.from_warehouse_id == from_warehouse_id and r.to_warehouse_id == to_warehouse_id
    ]

    best_routes = []

    for route in suitable_routes:
        transfers = [t for t in get_all_transfer_orders() if t.route_id == route.route_id]
        total_expected = sum(sum(i.quantity for i in t.items) for t in transfers)
        total_received = sum(sum(i.received_quantity for i in t.items) for t in transfers)

        avg_loss = ((total_expected - total_received) / total_expected * 100) if total_expected else 0
        reliability_score = route.reliability_rating * 0.7 + (100 - avg_loss) * 0.3

        best_routes.append({
            "route": route,
            "avg_loss": avg_loss,
            "reliability_score": reliability_score
        })

    best_routes.sort(key=lambda x: x["reliability_score"], reverse=True)
    return best_routes

def calculate_route_losses(route_id: int):
    """
    Считает статистику потерь по конкретному маршруту
    """
    orders = [o for o in get_all_transfer_orders() if o.route_id == route_id]
    if not orders:
        return None

    total_expected = sum(sum(i.quantity for i in o.items) for o in orders)
    total_received = sum(sum(i.received_quantity for i in o.items) for o in orders)

    loss_percentage = ((total_expected - total_received) / total_expected * 100) if total_expected > 0 else 0

    return {
        "route_id": route_id,
        "total_expected": total_expected,
        "total_received": total_received,
        "loss_percentage": loss_percentage
    }

#----
#рассчёт потерь при доставке
#----

import random
from models.transfer_order import TransferOrder
#from repositories.transfer_route_repository import update_transfer_route
from repositories.transfer_order_repository import get_transfer_order_by_id
from models.transfer_route import TransferRoute
from repositories.transfer_route_repository import get_transfer_route_by_id
from datetime import datetime
from repositories.material_repository import get_materials_by_order_id
from repositories.transfer_route_repository import update_transfer_route
from repositories.transfer_loss_repository import report_transfer_loss

def log_loss_to_file(order_id, route_id, material_id, expected_quantity, actual_quantity, loss_reason, recorded_by):
    """
    Записывает информацию о потере в .txt файл
    """
    with open("loss_reports.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        loss_percentage = round((expected_quantity - actual_quantity) / expected_quantity * 100, 2)

        f.write(f"[{timestamp}] Заказ #{order_id}, Маршрут #{route_id}, Материал #{material_id}\n")
        f.write(f"Ожидаемое количество: {expected_quantity}\n")
        f.write(f"Фактическое количество: {actual_quantity}\n")
        f.write(f"Потеря: {loss_percentage}%\n")
        f.write(f"Причина: {loss_reason}\n")
        f.write(f"Записал пользователь: {recorded_by}\n")
        f.write("-" * 60 + "\n")

def process_delivery_with_loss(db, order_id: int, route_id: int, user_id: int):
    """
    Обработка доставки с учётом возможной потери по каждому материалу
    """

    # Получаем маршрут
    route = get_transfer_route_by_id(route_id)
    if not route:
        raise ValueError(f"Маршрут #{route_id} не найден")

    current_rating = float(route.reliability_rating or 10.00)

    # Вероятность потери
    base_loss_rate = 0.05  # 5%
    loss_probability = base_loss_rate + (10.00 - current_rating) * 0.05
    loss_probability = min(max(loss_probability, 0.05), 1.00)  # от 5% до 100%

    print(f"Вероятность потери для маршрута #{route_id}: {loss_probability * 100:.2f}%")

    # Получаем материалы из заказа
    materials = get_materials_by_order_id(order_id)

    for material in materials:
        expected_quantity = float(material[1])

        # Случайная потеря
        if random.random() < loss_probability:
            loss_percent = random.uniform(0.01, 0.10)  # потеря от 1% до 10%
            actual_quantity = round(expected_quantity * (1 - loss_percent), 2)

            print(f"Потеря по материалу #{material[0]}: {expected_quantity} -> {actual_quantity}")

            # Уменьшение рейтинга маршрута
            new_rating = max(current_rating - 1.00, 1.00)
            #при ошибке сессий добавить db
            update_transfer_route(route_id, new_rating)
            report_transfer_loss(
                order_id,
                  route,
                material,
                expected_quantity,
                actual_quantity,
                'Случайная потеря',
                datetime.now(),
                user_id
            )
            # Логируем потерю
            log_loss_to_file(
                order_id=order_id,
                route_id=route_id,
                material_id=material.material_id,
                expected_quantity=expected_quantity,
                actual_quantity=actual_quantity,
                loss_reason=f"Случайная потеря ({loss_percent * 100:.2f}%)",
                recorded_by=user_id
            )

            # Обновляем остаток в OrderFilling
            material.quantity = actual_quantity
            db.add(material)
            db.flush()
