# views/warehouse_view.py

from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from services.warehouse_service import add_warehouse


class AddWarehouseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить склад")
        self.resize(300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.input_name = QLineEdit()
        self.input_type = QLineEdit()
        self.input_location = QLineEdit()
        self.input_description = QLineEdit()

        layout.addWidget(QLabel("Название"))
        layout.addWidget(self.input_name)
        layout.addWidget(QLabel("Тип (main/transit/workshop)"))
        layout.addWidget(self.input_type)
        layout.addWidget(QLabel("Адрес"))
        layout.addWidget(self.input_location)
        layout.addWidget(QLabel("Описание"))
        layout.addWidget(self.input_description)

        self.btn_save = QPushButton("Сохранить")
        self.btn_save.clicked.connect(self.save_warehouse)
        layout.addWidget(self.btn_save)

        self.setLayout(layout)

    def save_warehouse(self):
        name = self.input_name.text().strip()
        type = self.input_type.text().strip()
        location = self.input_location.text().strip()
        description = self.input_description.text().strip()

        if not name or not type:
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля")
            return

        try:
            added_warehouse = add_warehouse(name=name, type=type, location=location, description=description)
            QMessageBox.information(self, "Успех", f"Склад '{added_warehouse.name}' добавлен")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))