from PyQt6.QtWidgets import QWidget, QDialog, QHBoxLayout, QLabel, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt
from repositories.transfer_route_repository import get_all_transfer_routes
from repositories.warehouse_repository import get_warehouse_by_id
from repositories.material_repository import get_all_materials
from repositories.transfer_order_repository import create_transfer_order
from repositories.order_fill_repository import create_filling
from repositories.stock_balance_repository import get_stock_balance_by_warehouse_and_material, update_or_create_stock_balance
from models.user import User
from config.database import SessionLocal
from datetime import datetime

#заказ может создавать только менеджер производства и админ

class QuantityInputDialog(QDialog):
    def __init__(self, material_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Укажите количество")
        self.material_name = material_name
        self.quantity = None

        layout = QVBoxLayout()

        label = QLabel(f"Материал: {material_name}")
        self.input = QLineEdit()
        self.input.setPlaceholderText("Введите количество")

        btn_ok = QPushButton("ОК")
        btn_ok.clicked.connect(self.accept)

        layout.addWidget(label)
        layout.addWidget(self.input)
        layout.addWidget(btn_ok)

        self.setLayout(layout)

    def get_quantity(self):
        if self.exec() == QDialog.DialogCode.Accepted:
            try:
                self.quantity = float(self.input.text())
                return self.quantity
            except ValueError:
                return None
        return None




class MakeOrderView(QWidget):
    def __init__(self, user=None):
        super().__init__()
        if user is None:
            raise ValueError("Пользователь не передан")

        if not isinstance(user, User):
            raise TypeError(f"Ожидается объект User, получен {type(user)}")

        self.user = user  # ✅ Сохраняем объект пользователя
        print("Получен пользователь:", self.user.full_name)
        print("ID пользователя:", self.user.user_id)
        self.setWindowTitle("Создание заказа")
        self.setGeometry(300, 300, 800, 650)
        self.selected_route = None  # Добавляем инициализацию
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        allowed_roles = ["admin", "production_manager"]
        self.btn_create_order = QPushButton("Создать заказ")

        if self.user.role in allowed_roles:
            self.btn_create_order.clicked.connect(self.create_order)
        else:
            self.btn_create_order.setEnabled(False)
            self.btn_create_order.setText("Нет прав")
        title_label = QLabel("Введите информацию по заказу")
        layout.addWidget(title_label)

        # Раздел выбора маршрута
        label_one = QLabel("Выбор маршрута:")
        layout.addWidget(label_one)

        self.table_route = QTableWidget()
        self.table_route.setColumnCount(5)
        self.table_route.setHorizontalHeaderLabels(["ID маршрута", "Склад отправки", "Транзитный склад", "Склад приёмки", "Рейтинг"])
        layout.addWidget(self.table_route)
        self.load_data_route()

        self.btn_get_selected1 = QPushButton("Выбрать маршрут")
        self.btn_get_selected1.clicked.connect(self.get_selected_route)
        layout.addWidget(self.btn_get_selected1)

        self.label_route_result = QLabel("Выбранный маршрут: ")  # Переименовываем, чтобы избежать дублирования
        layout.addWidget(self.label_route_result)

        # Раздел выбора материалов
        label_materials = QLabel("Выбор материалов:")
        layout.addWidget(label_materials)

        self.table_materials = QTableWidget()
        self.table_materials.setColumnCount(3)  # Исправлено с 5 на 3, так как колонок три
        self.table_materials.setHorizontalHeaderLabels(["ID", "Название", "Тип"])
        self.table_materials.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)
        layout.addWidget(self.table_materials)
        self.load_data_material()

        self.btn_get_selected = QPushButton("Получить выбранные строки")
        self.btn_get_selected.clicked.connect(self.get_selected_materials)
        layout.addWidget(self.btn_get_selected)

        self.label_materials_result = QLabel("Выбранные материалы:")  # Переименовываем
        layout.addWidget(self.label_materials_result)

        self.btn_create_order = QPushButton("Создать заказ")
        self.btn_create_order.clicked.connect(self.create_order)
        layout.addWidget(self.btn_create_order)

        self.setLayout(layout)

    def load_data_route(self):
        self.all_routes = get_all_transfer_routes()
        if not self.all_routes:
            self.table_route.setRowCount(0)
            return

        self.displayed_routes = self.all_routes.copy()
        self.update_table_routes()

    def load_data_material(self):
        self.all_materials = get_all_materials()
        if not self.all_materials:
            self.table_materials.setRowCount(0)
            return

        self.displayed_materials = self.all_materials.copy()
        self.update_table_materials()

    def update_table_routes(self):
        headers = ["ID маршрута", "Склад отправки", "Склад приёмки", "Транзитный склад", "Рейтинг"]
        self.table_route.setColumnCount(len(headers))
        self.table_route.setHorizontalHeaderLabels(headers)
        self.table_route.setRowCount(len(self.displayed_routes))

        for row_idx, order in enumerate(self.displayed_routes):
            data = [
                str(order.route_id),
                str(order.from_warehouse_id),
                str(order.to_warehouse_id),
                str(order.transit_warehouse_id),
                str(order.reliability_rating)
            ]

            # Безопасное получение информации о складах
            try:
                self.from_w = get_warehouse_by_id(data[1])
                to_w = get_warehouse_by_id(data[2])
                transit_w = get_warehouse_by_id(data[3])

                data[1] = self.from_w.location if self.from_w else "Неизвестно"
                data[2] = to_w.location if to_w else "Неизвестно"
                data[3] = transit_w.location if transit_w else "Неизвестно"
            except Exception as e:
                print(f"Ошибка при получении данных склада: {e}")
                data[1] = data[2] = data[3] = "Ошибка"

            for col_idx, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table_route.setItem(row_idx, col_idx, item)

    def update_table_materials(self):
        headers = ["ID", "Название", "Тип"]
        self.table_materials.setColumnCount(len(headers))
        self.table_materials.setHorizontalHeaderLabels(headers)
        self.table_materials.setRowCount(len(self.displayed_materials))

        for row_idx, order in enumerate(self.displayed_materials):
            data = [
                str(order.material_id),
                str(order.name),
                str(order.type)
            ]
            for col_idx, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table_materials.setItem(row_idx, col_idx, item)

    def get_selected_route(self):
        selected_items = self.table_route.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            route_id = self.table_route.item(row, 0).text()
            from_warehouse = self.table_route.item(row, 1).text()
            self.selected_route = {
                "route_id": int(route_id),
                "from_warehouse": from_warehouse
            }
            #self.selected_route = f"ID: {route_id}, Отправка: {from_warehouse}"
            self.label_route_result.setText(f"Выбранный маршрут: {self.selected_route}")
        else:
            self.label_route_result.setText("Маршрут не выбран")

    def get_selected_materials(self):
        selected_rows = set()
        for item in self.table_materials.selectedItems():
            selected_rows.add(item.row())

        selected_materials = []

        for row in sorted(selected_rows):
            material_id = self.table_materials.item(row, 0).text()
            name = self.table_materials.item(row, 1).text()
            type = self.table_materials.item(row, 2).text()
            self.balance = get_stock_balance_by_warehouse_and_material(self.from_w.warehouse_id, material_id)
            print(self.balance.quantity)
            dialog = QuantityInputDialog(name, self)
            self.quantity = dialog.get_quantity()
            while (self.quantity > int(self.balance.quantity)):
                dialog = QuantityInputDialog(name, self)
                self.quantity = dialog.get_quantity()

            if self.quantity is not None and self.quantity > 0:
                selected_materials.append({
                    "material_id": int(material_id),
                    "name": name,
                    "type": type,
                    "quantity": self.quantity
                })

        self.label_materials_result.setText(f"Выбрано материалов: {len(selected_materials)}")
        print("Выбранные материалы с количеством:", selected_materials)
        return selected_materials

    

    def create_order(self):
        if not isinstance(self.user, User):
            QMessageBox.critical(self, "Ошибка", "Пользователь не авторизован")
            return

        selected_materials = self.get_selected_materials()
        if not selected_materials:
            QMessageBox.information(self, "Информация", "Материалы не выбраны")
            return

        db = SessionLocal()
        try:
            # 1. Создаём заказ
            route_id = self.selected_route["route_id"]
            order_id = create_transfer_order(db,route_id, 'created', datetime.now(),self.user.user_id)
            print(f"order_id '{order_id}")
            db.flush()
            # 2. Добавляем материалы
            for material in selected_materials:
                create_filling(db,order_id, material['material_id'], material['quantity'])

            # 3. Обновляем остатки на складе
            for material in selected_materials:
                update_or_create_stock_balance(
                    db,
                    warehouse_id=self.from_w.warehouse_id,
                    material_id=material['material_id'],
                    quantity=material['quantity']
                )
            from repositories.material_repository import get_materials_by_order_id
            from services.report_service import save_order_document,generate_order_content
            from models.transfer_order import TransferOrder

            order = db.query(TransferOrder).get(order_id)
            materials = get_materials_by_order_id(order_id)
            content = generate_order_content(order, materials)
            save_order_document(order_id, "order", content)
            
            db.commit()
            QMessageBox.information(self, "Успех", f"Заказ #{order_id} создан")
        except Exception as e:
            db.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать заказ:\n{e}")
        finally:
            db.close()


    def create_input_widget(self):
        input_container = QWidget()
        layout = QHBoxLayout()
        input_container.setLayout(layout)
        return input_container