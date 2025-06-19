# views/report_view.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from services.report_service import generate_stock_report, generate_transfer_report
from utils.file_utils import save_report_to_txt


class ReportView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Отчёты")
        self.resize(700, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        layout.addWidget(self.report_text)

        self.btn_stock = QPushButton("Показать остатки")
        self.btn_stock.clicked.connect(lambda: self.show_report(generate_stock_report()))

        self.btn_transfer = QPushButton("Показать перемещения")
        self.btn_transfer.clicked.connect(lambda: self.show_report(generate_transfer_report()))

        self.btn_save = QPushButton("Сохранить в TXT")
        self.btn_save.clicked.connect(self.save_current_report)

        layout.addWidget(self.btn_stock)
        layout.addWidget(self.btn_transfer)
        layout.addWidget(self.btn_save)
        self.setLayout(layout)

        self.current_report = []

    def show_report(self, report_lines):
        self.current_report = report_lines
        self.report_text.setPlainText("\n".join(report_lines))

    def save_current_report(self):
        if not self.current_report:
            print("Нет данных для сохранения")
            return
        save_report_to_txt(self.current_report, "custom_report.txt")
        print("Произвольный отчёт сохранён как 'custom_report.txt'")