from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from services.report_service import generate_stock_report
from utils.file_utils import save_report_to_txt


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