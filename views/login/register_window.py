# views/register_window.py

from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setGeometry(450, 300, 400, 250)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label_username = QLabel("Логин:")
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Введите логин")

        self.label_password = QLabel("Пароль:")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Введите пароль")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.label_fullname = QLabel("ФИО:")
        self.input_fullname = QLineEdit()
        self.input_fullname.setPlaceholderText("Введите ФИО")

        self.label_role = QLabel("Роль:")
        self.combo_role = QComboBox()
        self.combo_role.addItems(["admin", "warehouse_manager", "production_manager", "logistics"])

        self.btn_register = QPushButton("Зарегистрироваться")
        self.btn_register.clicked.connect(self.handle_register)

        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.label_fullname)
        layout.addWidget(self.input_fullname)
        layout.addWidget(self.label_role)
        layout.addWidget(self.combo_role)
        layout.addWidget(self.btn_register)

        self.setLayout(layout)

    def handle_register(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()
        full_name = self.input_fullname.text().strip()
        role = self.combo_role.currentText()

        if not all([username, password, full_name]):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            from repositories.user_repository import create_user
            created_user = create_user(username, password, full_name, role)
            QMessageBox.information(self, "Успех", f"Пользователь {created_user.full_name} успешно зарегистрирован!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось зарегистрировать пользователя:\n{str(e)}")