# views/documents/documents_view.py

from PyQt6.QtWidgets import QDialog, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from repositories.transfer_order_repository import get_transfer_order_by_id, get_all_transfer_orders
from repositories.material_repository import get_materials_by_order_id
from repositories.transfer_loss_repository import get_losses_by_order_id
from config.database import SessionLocal
import os
from PyQt6.QtWidgets import QComboBox, QTextEdit

#добавь в таблицу TransferLosses в SQL колонку recorded_by_id потому
#что сейчас её там нет и выдаётся ошибка

class DocumentView(QDialog):  # ← Теперь это диалог
    def __init__(self, parent=None, order_id: int = None):
        super().__init__(parent)
        self.setWindowTitle("Документы по заказу")
        self.resize(800, 600)  # размер окна
        self.order_id = order_id or None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Выберите заказ для просмотра документов")
        layout.addWidget(self.title_label)

        # Список заказов
        self.order_combo = QComboBox()
        self.orders = get_all_transfer_orders()
        for order in self.orders:
            self.order_combo.addItem(f"Заказ #{order.order_id}", order.order_id)
        self.order_combo.currentIndexChanged.connect(self.on_order_changed)
        layout.addWidget(self.order_combo)

        # Список типов документов
        self.doc_type_combo = QComboBox()
        self.doc_type_combo.addItems(["order", "shipment", "receipt"])
        self.doc_type_combo.currentTextChanged.connect(self.load_report)
        layout.addWidget(self.doc_type_combo)

        # Просмотр отчёта
        self.report_view = QTextEdit()
        self.report_view.setReadOnly(True)
        layout.addWidget(self.report_view)

        self.setLayout(layout)

        # Установить выбранный заказ, если передан
        if self.order_id:
            idx = self.order_combo.findData(self.order_id)
            if idx != -1:
                self.order_combo.setCurrentIndex(idx)
        else:
            self.on_order_changed()

    def on_order_changed(self):
        self.order_id = self.order_combo.currentData()
        if self.order_id:
            self.title_label.setText(f"Документы по заказу #{self.order_id}")
            self.load_report()
        else:
            self.title_label.setText("Выберите заказ для просмотра документов")
            self.report_view.clear()

    def load_report(self):
        if not self.order_id:
            self.report_view.setText("Сначала выберите заказ.")
            return
        doc_type = self.doc_type_combo.currentText()
        path = os.path.join("reports", "orders", f"ORDER_{self.order_id}", f"{doc_type}.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.report_view.setText(f.read())
        else:
            self.report_view.setText("Документ не найден.")

    def select_order(self):
        # Здесь можно вызвать диалог выбора заказа или просто ввести ID
        from PyQt6.QtWidgets import QInputDialog

        order_id, ok = QInputDialog.getInt(self, "Введите номер заказа", "Order ID:")
        if ok and order_id > 0:
            self.order_id = order_id
            self.title_label.setText(f"Документы по заказу #{self.order_id}")
            self.load_order_details(order_id)

    def load_order_details(self, order_id: int):
        """
        Загрузка информации о заказе и его документах
        """
        from models.transfer_order import TransferOrder
        from models.material import Material

        db = SessionLocal()
        try:
            materials = get_materials_by_order_id(order_id)
            losses = get_losses_by_order_id(db, order_id)

            loss_dict = {
                loss.material_id: float(loss.quantity) for loss in losses
            }

            self.table.setRowCount(len(materials))
            for row_idx, (material_id, quantity) in enumerate(materials):
                # Получаем название материала по его ID
                material_obj = db.query(Material).get(material_id)
                name = material_obj.name if material_obj else "Неизвестен"

                self.table.setItem(row_idx, 0, QTableWidgetItem(str(material_id)))
                self.table.setItem(row_idx, 1, QTableWidgetItem(name))
                self.table.setItem(row_idx, 2, QTableWidgetItem(str(quantity)))

                # Потери
                loss_amount = loss_dict.get(material_id, 0)
                self.table.setItem(row_idx, 3, QTableWidgetItem(str(loss_amount)))
        finally:
            db.close()