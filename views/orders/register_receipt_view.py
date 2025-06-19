from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton,QMessageBox
from PyQt6.QtCore import Qt
from repositories.transfer_order_repository import get_all_transfer_orders
from config.database import SessionLocal
class RegisterReceiptView(QWidget):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Зарегистрировать приемку")
        self.setGeometry(100, 60, 600, 400)
        self.user = user
        self.selected_order_id = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Дата создания", "Статус"])
        self.table.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)
        self.table.cellClicked.connect(self.on_row_selected)
        layout.addWidget(self.table)
        self.load_orders()

        self.btn_send = QPushButton("Принять заказ")
        self.btn_send.clicked.connect(self.receive_selected_order)
        layout.addWidget(self.btn_send)

        allowed_roles = ["admin", "warehouse_manager"]
        if self.user.role not in allowed_roles:
            self.btn_send.setEnabled(False)
            self.btn_send.setText("Нет прав: Приемка")

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

    def receive_selected_order(self):
        if not hasattr(self, 'selected_order_id') or not self.selected_order_id:
            return

        from datetime import datetime
        from models.transfer_order import TransferOrder
        from repositories.transfer_order_repository import receive_shipment
        from repositories.order_fill_repository import create_filling
        from services.route_service import process_delivery_with_loss
        from repositories.transfer_order_repository import get_transfer_order_by_id

        #order = get_transfer_order_by_id(self.selected_order_id)
        db = SessionLocal()
        try:
            order_id = self.selected_order_id
            transfer_order = db.query(TransferOrder).get(order_id)
            if not transfer_order:
                raise ValueError(f"Заказ #{order_id} не найден")
            route_id = transfer_order.route_id
            if not route_id:
                raise ValueError("У заказа нет маршрута")
            result = process_delivery_with_loss(db, order_id, route_id, self.user.user_id)
            receive_shipment(self.selected_order_id)
            QMessageBox.information(self, "Успех", "Заказ принят")
            self.close()
        except Exception as e:
            QMessageBox.critical(self,"Ошибка", f"Не удалось принять заказ:\n{e}")
        finally: db.close()