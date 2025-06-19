from PyQt6.QtWidgets import QWidget, QMessageBox, QComboBox, QDialog, QLabel, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from repositories.warehouse_repository import get_all_warehouses, update_warehouse

class WarehouseInputDialog(QDialog):
    def __init__(self, warehouse_id, name, location, type, is_active, parent=None):
        super().__init__()
        self.setWindowTitle("Изменение информации о складе")
        self.warehouse_id = warehouse_id

        layout = QVBoxLayout()

        label_name = QLabel(f"Склад {name}")
        label_location = QLabel(f"Местоположение: {location}")
        self.input_location = QLineEdit()
        self.input_location.setPlaceholderText("Измените адрес")
        
        label_type = QLabel(f"Тип склада: {type}")
        self.input_type = QComboBox()
        self.input_type.addItems([
            "production",
            "transit",
            "finished_products"
        ])
        #self.input_type.setPlaceholderText("Измените адрес")
        if is_active == "активен":
            is_active_str = "активен"
        else:
            is_active_str = "не активен"
        label_is_active = QLabel(f"Активность: {is_active_str}")
        self.input_status = QComboBox()
        self.input_status.addItems([
            "активен",
            "не активен"
        ])
        self.input_status.setPlaceholderText("Измените статус")

        btn_ok = QPushButton("ОК")
        btn_ok.clicked.connect(self.accept)

        layout.addWidget(label_name)
        layout.addWidget(label_location)
        layout.addWidget(self.input_location)
        layout.addWidget(label_type)
        layout.addWidget(self.input_type)
        layout.addWidget(label_is_active)
        layout.addWidget(self.input_status)
        layout.addWidget(btn_ok)

        self.setLayout(layout)

    def get_data(self, location):
        if self.exec() == QDialog.DialogCode.Accepted:
            try:
                if self.input_location.text() == "" :
                    self.location = location
                else:
                    self.location = self.input_location.text()
                self.type = self.input_type.currentText()
                status_text = self.input_status.currentText()
                self.is_active = (status_text == "активен")

                return self.location, self.type, self.is_active
            except ValueError:
                return None
        return None

class WarehouseView(QWidget):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Управление складами")
        self.setGeometry(300, 300, 800, 350)
        self.user = user
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID маршрута", "Название", "Тип", "Местоположение", "Активность"])
        layout.addWidget(self.table)
        self.load_data()

        self.btn_get_selected = QPushButton("Изменить информацию о выбранном складе")
        self.btn_get_selected.clicked.connect(self.get_selected)
        layout.addWidget(self.btn_get_selected)

        self.label_result = QLabel("Измененная информация:")
        layout.addWidget(self.label_result)

        self.setLayout(layout)

    def load_data(self):
        self.all_warehouses = get_all_warehouses()
        if not self.all_warehouses:
            self.table.setRowCount(0)
            return
        self.displayed_warehouses = self.all_warehouses.copy()
        self.update_table()

    def update_table(self):
        headers = ["ID маршрута", "Название", "Тип", "Местоположение", "Активность"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(self.displayed_warehouses))

        for row_idx, warehouse in enumerate(self.displayed_warehouses):
            data = [
                str(warehouse.warehouse_id),
                str(warehouse.name),
                str(warehouse.type),
                str(warehouse.location),
                str(warehouse.is_active)
            ]
            if warehouse.is_active:
                data[4] = "активен"
            else:
                data[4] = "не активен"
            for col_idx, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row_idx, col_idx, item)

    def get_selected(self):
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())

        selected_warehouse = []

        for row in sorted(selected_rows):
            warehouse_id = self.table.item(row, 0).text()
            name = self.table.item(row, 1).text()
            type = self.table.item(row, 2).text()
            location = self.table.item(row, 3).text()
            is_active = self.table.item(row, 4).text()

            dialog = WarehouseInputDialog(warehouse_id, name, location, type, is_active, self)

            data = dialog.get_data(location)
            if data[0] is not None:
                location = data[0]
            if data[1] is not None:
                type = data[1]
            if data[2] is not None:
                is_active = data[2]
            try:
                update_warehouse(
                warehouse_id=warehouse_id,
                name=name,
                type=type,
                location=location,
                is_active=is_active
            )
                selected_warehouse.append({
                    "warehouse_id": int(warehouse_id),
                    "name": name,
                    "type": type,
                    "location": location,
                    "is_active": is_active
                })
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось обновить склад {warehouse_id}:\n{e}")

        self.label_result.setText(f"Измененная информация: {selected_warehouse}")
        return selected_warehouse

