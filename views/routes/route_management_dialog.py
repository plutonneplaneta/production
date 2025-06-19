# views/routes/route_management_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QHBoxLayout, QMessageBox, QLineEdit
)
from PyQt6.QtCore import Qt



class RouteManagementDialog(QDialog):
    def __init__(self, parent=None, route=None):
        """
        :param parent: родительское окно
        :param route: объект маршрута (если редактирование)
        """
        super().__init__(parent)
        self.route = route
        self.setWindowTitle("Добавить/Изменить маршрут")
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Поля выбора складов
        self.from_warehouse_combo = QComboBox()
        self.to_warehouse_combo = QComboBox()
        self.transit_warehouse_combo = QComboBox()
        self.transit_warehouse_combo.addItem("-- Нет --", userData=None)

        # Загрузка данных из репозитория
        from repositories.warehouse_repository import get_all_warehouses
        warehouses = get_all_warehouses()

        for wh in warehouses:
            self.from_warehouse_combo.addItem(wh.name, userData=wh.warehouse_id)
            self.to_warehouse_combo.addItem(wh.name, userData=wh.warehouse_id)
            self.transit_warehouse_combo.addItem(wh.name, userData=wh.warehouse_id)

        # Если это редактирование — устанавливаем текущие значения
        if self.route:
            index_from = self.from_warehouse_combo.findData(self.route.from_warehouse_id)
            index_to = self.to_warehouse_combo.findData(self.route.to_warehouse_id)
            index_transit = self.transit_warehouse_combo.findData(self.route.transit_warehouse_id)
            

            self.from_warehouse_combo.setCurrentIndex(index_from if index_from != -1 else 0)
            self.to_warehouse_combo.setCurrentIndex(index_to if index_to != -1 else 0)
            self.transit_warehouse_combo.setCurrentIndex(index_transit if index_transit != -1 else 0)
            
        # Форма
        layout.addWidget(QLabel("Склад отправки:"))
        layout.addWidget(self.from_warehouse_combo)

        layout.addWidget(QLabel("Транзитный склад:"))
        layout.addWidget(self.transit_warehouse_combo)

        layout.addWidget(QLabel("Склад прибытия:"))
        layout.addWidget(self.to_warehouse_combo)

        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Введите время доставки (в часах)")
        layout.addWidget(QLabel("Время доставки (часов):"))
        layout.addWidget(self.duration_input)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def get_data(self):
        """Возвращает данные из полей"""
        try:
            duration_hours = int(self.duration_input.text())
        except ValueError:
            duration_hours = 24
        return {
            "from_warehouse_id": self.from_warehouse_combo.currentData(),
            "to_warehouse_id": self.to_warehouse_combo.currentData(),
            "transit_warehouse_id": self.transit_warehouse_combo.currentData(),
            "duration_hours": duration_hours
        }