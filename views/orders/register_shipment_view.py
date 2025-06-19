from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton,QMessageBox
from PyQt6.QtCore import Qt
from repositories.transfer_order_repository import get_all_transfer_orders, cancel_shipment
from models.user import User

class RegisterShipmentView(QWidget):
    def __init__(self, user=None):
        super().__init__()
        if user is None:
            raise ValueError("Пользователь не передан")

        if not isinstance(user, User):
            print(user)
            raise TypeError(f"Ожидается объект User, получен {type(user)}")

        self.setWindowTitle("Зарегистрировать отправку")
        self.setGeometry(100, 60, 600, 400)
        self.user = user
        self.selected_order_id = None

        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Дата создания", "Статус"])
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.cellClicked.connect(self.on_row_selected)
        layout.addWidget(self.table)
        self.load_orders()

        self.btn_send = QPushButton("Отправить заказ")
        self.btn_send.setEnabled(False)
        self.btn_send.clicked.connect(self.send_selected_order)
        layout.addWidget(self.btn_send)

        self.btn_cancel = QPushButton("Отменить заказ")
        self.btn_cancel.clicked.connect(self.cancel_selected_order)
        layout.addWidget(self.btn_cancel)

        # Проверка прав пользователя
        allowed_roles = ["admin", "warehouse_manager"]

        if self.user.role in allowed_roles:
            self.btn_send.setEnabled(True)
            self.btn_cancel.setEnabled(True)
        else:
            self.btn_send.setToolTip("Нет прав для регистрации отправки")
            self.btn_cancel.setToolTip("Нет прав для отмены заказа")
            self.btn_send.setText("Нет прав: отправка")
            self.btn_cancel.setText("Нет прав: отмена")

        self.setLayout(layout)

    def load_orders(self):
        orders = get_all_transfer_orders()
        self.table.setRowCount(len(orders))

        for row_idx, order in enumerate(orders):
            data = [
                str(order.order_id),
                str(order.created_at),
                order.status
            ]

            for col_idx, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row_idx, col_idx, item)

    def on_row_selected(self, row, column):
        try:
            self.selected_order_id = int(self.table.item(row, 0).text())
            print(f"Выбран заказ #{self.selected_order_id}")
            self.btn_send.setEnabled(True)
        except Exception as e:
            print("Ошибка при выборе заказа:", e)
            self.btn_send.setEnabled(False)

    def send_selected_order(self):
        if not hasattr(self, 'selected_order_id') or not self.selected_order_id:
            return

        from datetime import date
        from repositories.transfer_order_repository import update_shipment_data
        from config.database import SessionLocal
        from repositories.transfer_route_repository import get_transfer_route_by_order_id
        from repositories.stock_balance_repository import subtract_material_from_warehouse
        from repositories.material_repository import get_materials_by_order_id


        order_id = self.selected_order_id
        route = get_transfer_route_by_order_id(order_id)
        materials = get_materials_by_order_id(order_id)
        print(f"route.from_warehouse_id {route.from_warehouse_id}")

        try:
            for material in materials:
                expected_quantity = float(material[1])
                material_id = material[0]
                print(f"material_id {material_id}")

                subtract_material_from_warehouse(route.from_warehouse_id, material_id, expected_quantity)
            update_shipment_data(self.selected_order_id)
            QMessageBox.information(self, "Успех", "Отправка зарегистрирована")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось зарегистрировать отправку:\n{e}")


    def cancel_selected_order(self):
        if not hasattr(self, 'selected_order_id') or not self.selected_order_id:
            return

        try:
            cancel_shipment(self.selected_order_id)
            QMessageBox.information(self, "Успех", "Заказ отменён")
            self.close()
        except Exception as e:
            QMessageBox.critical(self,"Ошибка", f"Не удалось отменить заказ:\n{e}")