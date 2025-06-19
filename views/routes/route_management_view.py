from PyQt6.QtWidgets import QComboBox,QVBoxLayout,QLabel,QHBoxLayout,QDialog,QWidget, QVBoxLayout, QTextEdit, QPushButton
from services.report_service import generate_stock_report
from utils.file_utils import save_report_to_txt
from PyQt6.QtCore import Qt

# views/routes/route_management_view.py

from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton,QMessageBox
from views.routes.route_management_dialog import RouteManagementDialog
from repositories.transfer_route_repository import get_all_transfer_routes, create_transfer_route, update_transfer_route,get_transfer_route_by_id, update_transfer_route_with_new, delete_transfer_route
from repositories.warehouse_repository import get_warehouse_name_by_id
 
class RouteView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Управление маршрутами")
        self.setGeometry(100, 100, 700, 500)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()

        # Таблица маршрутов
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Склад отправки", "Склад транзита", "Склад приёмки", "Рейтинг маршрута"])
        layout.addWidget(self.table)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Добавить маршрут")
        self.btn_edit = QPushButton("Редактировать маршрут")
        self.btn_delete = QPushButton("Удалить маршрут")

        self.btn_add.clicked.connect(self.open_add_dialog)
        self.btn_edit.clicked.connect(self.open_edit_dialog)
        self.btn_delete.clicked.connect(self.open_delete_dialog)

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_data(self):
        routes = get_all_transfer_routes()
        self.table.setRowCount(len(routes))

        for row_idx, route in enumerate(routes):
            data = [
                str(route.route_id),
                str(get_warehouse_name_by_id(route.from_warehouse_id)),
                str(get_warehouse_name_by_id(route.transit_warehouse_id)),
                str(get_warehouse_name_by_id(route.to_warehouse_id)),
                str(route.reliability_rating)
            ]
            for col_idx, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row_idx, col_idx, item)

    def open_add_dialog(self):
        dialog = RouteManagementDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                create_transfer_route(**data)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить маршрут:\n{e}")

    def open_edit_dialog(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        route_id = int(selected_items[0].text())
        route = get_transfer_route_by_id(route_id)

        dialog = RouteManagementDialog(self, route=route)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_data()
            try:
                update_transfer_route_with_new(route_id, updated_data)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось обновить маршрут:\n{e}")

    def open_delete_dialog(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите удалить выбранный маршрут?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            route_id = int(selected_items[0].text())
            try:
                delete_transfer_route(route_id)
                self.load_data()  # обновляем таблицу
                QMessageBox.information(self, "Успех", f"Маршрут #{route_id} удален")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить маршрут:\n")

class StockView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Складские остатки")
        self.resize(600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        layout.addWidget(self.report_text)

        self.btn_load = QPushButton("Загрузить остатки по основному складу")
        self.btn_load.clicked.connect(self.load_stock_report)
        layout.addWidget(self.btn_load)

        self.btn_save = QPushButton("Сохранить отчёт в TXT")
        self.btn_save.clicked.connect(self.save_stock_report)
        layout.addWidget(self.btn_save)

        self.setLayout(layout)

    def load_stock_report(self):
        try:
            report_lines = generate_stock_report(warehouse_id=1)
            self.report_text.setPlainText("\n".join(report_lines))
        except Exception as e:
            self.report_text.setPlainText(f"Ошибка загрузки данных:\n{str(e)}")

    def save_stock_report(self):
        report_lines = generate_stock_report(warehouse_id=1)
        success = save_report_to_txt(report_lines, "stock_report.txt")
        if success:
            print("Отчёт сохранён как 'stock_report.txt'")
        else:
            print("Не удалось сохранить отчёт")