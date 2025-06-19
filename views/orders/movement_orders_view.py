from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from repositories.transfer_order_repository import get_all_transfer_orders

class OrderView(QWidget):
    def __init__(self, parent=None, user=None):
        super().__init__()
        self.setWindowTitle("Заказы перемещения")
        self.setGeometry(300, 300, 800, 350)
        self.user = user
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по номеру заказа")
        self.search_input.textChanged.connect(self.filter_table)
        layout.addWidget(self.search_input)

        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        self.table.setColumnCount(11)
        layout.addWidget(self.table)
        # Загружаем данные
        self.load_data()
 
        self.table.sortByColumn(3, Qt.SortOrder.AscendingOrder)
        self.table.sortByColumn(4, Qt.SortOrder.AscendingOrder)
        self.table.sortByColumn(7, Qt.SortOrder.AscendingOrder)
        self.table.sortByColumn(8, Qt.SortOrder.AscendingOrder)

        self.btn_make_order = QPushButton("Создать заказ")
        self.btn_make_order.clicked.connect(self.make_order)
        layout.addWidget(self.btn_make_order)

        self.btn_register_shipment = QPushButton("Зарегистрировать отправку")
        self.btn_register_shipment.clicked.connect(self.register_shipment)
        layout.addWidget(self.btn_register_shipment)

        self.btn_register_receipt = QPushButton("Зарегистрировать приемку")
        self.btn_register_receipt.clicked.connect(self.register_receipt)
        layout.addWidget(self.btn_register_receipt)
        self.setLayout(layout)

    def make_order(self):
        from .make_order_view import MakeOrderView
        self.make_order_view = MakeOrderView(user=self.user)
        self.make_order_view.show()
    def register_shipment(self):
        from .register_shipment_view import RegisterShipmentView
        self.register_shipment_view = RegisterShipmentView(user=self.user)
        self.register_shipment_view.show()
    def register_receipt(self):
        from .register_receipt_view import RegisterReceiptView
        self.register_receipt_view = RegisterReceiptView(user=self.user)
        self.register_receipt_view.show()

    def load_data(self):
        self.all_orders = get_all_transfer_orders()
        #print("Количество заказов:", len(orders))
        if not self.all_orders:
            self.table.setRowCount(0)
            return

        self.displayed_orders = self.all_orders.copy()
        self.update_table()

    def filter_table(self):
        search_text = self.search_input.text().lower()

        self.displayed_orders = [
            order for order in self.all_orders
            if search_text in str(order.order_id).lower()
        ]

        self.update_table()


    def update_table(self):
        headers = ["Номер", "Маршрут", "Дата отправки", "Дата приемки", "Статус", "Пользователь", "Дата создания", "Дата изменения"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(self.displayed_orders))

        for row_idx, order in enumerate(self.displayed_orders):
            data = [
                str(order.order_id),
                str(order.route_id),
                str(order.shipment_date),
                str(order.arrival_date),
                str(order.status),
                str(order.created_by),
                str(order.created_at),
                str(order.updated_at)
            ]

            for col_idx, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row_idx, col_idx, item)

