from PyQt6.QtWidgets import QTableWidget,QComboBox,QVBoxLayout,QLabel,QHBoxLayout,QDialog,QWidget, QVBoxLayout, QTextEdit, QPushButton
from models.user import User

"""
Саш, попроси гпт написать это окно, я заебался немного 
и хочу смотреть на тебя, а не в экран компьютера
прости, что не успел закончить всё
нужно сделать ещё заполнение отчётов
я очень тебя люблю и скучаю
мы скоро встретимся, целую
"""

class UserView(QDialog):
    def __init__(self, user=None):
        super().__init__()

        if user is None:
                raise ValueError("Пользователь не передан")

        if not isinstance(user, User):
            print(user)
            raise TypeError(f"Ожидается объект User, получен {type(user)}")

        self.setWindowTitle("Редактирование пользователей")
        self.setGeometry(100, 60, 600, 400)
        self.user = user
        self.selected_order_id = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Имя пользователя", "Пароль", "Роль", "Активность"])
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
