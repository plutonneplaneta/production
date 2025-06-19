from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from repositories.user_repository import get_user_by_username
from models.user import User
from views.login.register_window import RegisterWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setGeometry(450, 300, 500, 250)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label_header = QLabel("Информационная система управления производством")
        self.label_header.setStyleSheet("""
            font-weight: bold;
            color: #5B5B5B;
            font-size: 16px;
            padding: 10px;
        """)

        self.label_username = QLabel("Логин:")
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Введите логин")

        self.label_password = QLabel("Пароль:")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Введите пароль")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_login = QPushButton("Войти")
        self.btn_login.clicked.connect(self.handle_login)

        self.btn_register = QPushButton("Зарегистрироваться")
        self.btn_register.clicked.connect(self.open_register_window)

        layout.addWidget(self.label_header)
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_register)

        self.setLayout(layout)

    def handle_login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        user = get_user_by_username(username)
        if user and user.password == password:
            QMessageBox.information(self, "Успех", "Вы вошли в систему")
            self.close()
            from views.main_window import MainWindow
            self.main_window = MainWindow(user)
            self.main_window.show()
            print("user:", user)
            print("type(user):", type(user))

        else:
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль")

    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()