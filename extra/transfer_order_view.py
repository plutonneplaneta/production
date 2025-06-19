# views/transfer_order_view.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QComboBox, QLineEdit, QLabel
from services.report_service import generate_transfer_report
from utils.file_utils import save_report_to_txt
from services.route_service import find_best_routes
from services.warehouse_service import list_all_warehouses

class TransferOrderView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Перемещения материалов")
        self.resize(600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        layout.addWidget(self.report_text)

        self.btn_load = QPushButton("Загрузить отчёт по перемещениям")
        self.btn_load.clicked.connect(self.load_transfer_report)
        layout.addWidget(self.btn_load)

        self.btn_save = QPushButton("Сохранить отчёт в TXT")
        self.btn_save.clicked.connect(self.save_transfer_report)
        layout.addWidget(self.btn_save)

        self.route_combo = QComboBox()
        self.material_combo = QComboBox()
        self.quantity_input = QLineEdit()

        # Склад отправления
        layout.addWidget(QLabel("Склад отправления"))
        self.input_from_warehouse = QComboBox()
        self.load_warehouses(self.input_from_warehouse)

        # Склад получения
        layout.addWidget(QLabel("Склад получения"))
        self.input_to_warehouse = QComboBox()
        self.load_warehouses(self.input_to_warehouse)

        layout.addWidget(self.input_from_warehouse)
        layout.addWidget(self.input_to_warehouse)

        # Кнопка выбора маршрута
        self.btn_load_routes = QPushButton("Показать маршруты")
        self.btn_load_routes.clicked.connect(self.update_suggested_routes)
        layout.addWidget(self.btn_load_routes)

        #self.input_from_warehouse.currentIndexChanged.connect(self.update_suggested_routes)
        #self.input_to_warehouse.currentIndexChanged.connect(self.update_suggested_routes)

        layout.addWidget(QLabel("Выберите маршрут"))
        layout.addWidget(self.route_combo)
        layout.addWidget(QLabel("Материал"))
        layout.addWidget(self.material_combo)
        layout.addWidget(QLabel("Количество"))
        layout.addWidget(self.quantity_input)

        self.setLayout(layout)

    def load_transfer_report(self):
        report_lines = generate_transfer_report()
        self.report_text.setPlainText("\n".join(report_lines))

    def save_transfer_report(self):
        report_lines = generate_transfer_report()
        save_report_to_txt(report_lines, "transfer_report.txt")
        print("Отчёт по перемещениям сохранён как 'transfer_report.txt'")

    def suggest_best_routes(self):
        from_warehouse_id = self.input_from_warehouse.currentData()
        to_warehouse_id = self.input_to_warehouse.currentData()

        best_routes = find_best_routes(from_warehouse_id, to_warehouse_id)

        self.route_combo.clear()
        for item in best_routes:
            route = item["route"]
            text = f"Маршрут {route.from_warehouse.name} → {route.to_warehouse.name} | Надежность: {item['reliability_score']:.2f}"
            self.route_combo.addItem(text, route.route_id)


    def update_suggested_routes(self):
        from_warehouse_id = self.input_from_warehouse.currentData()
        to_warehouse_id = self.input_to_warehouse.currentData()

        if from_warehouse_id and to_warehouse_id:
            best_routes = find_best_routes(from_warehouse_id, to_warehouse_id)
            self.route_combo.clear()
            for item in best_routes:
                route = item["route"]
                score = item["reliability_score"]
                self.route_combo.addItem(f"{route.from_warehouse.name} → {route.to_warehouse.name} | Надёжность: {score:.1f}", route.route_id)

    def load_warehouses(self, combobox: QComboBox):
        """
        Загружает список складов в указанный QComboBox
        """
        try:
            warehouses = list_all_warehouses()  # Получаем данные через сервис
            for warehouse in warehouses:
                combobox.addItem(f"{warehouse.name} ({warehouse.type})", userData=warehouse.warehouse_id)
        except Exception as e:
            print(f"Ошибка загрузки складов: {e}")