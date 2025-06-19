from PyQt6.QtWidgets import QTableWidgetItem,QMessageBox,QLineEdit,QTableWidget,QComboBox,QVBoxLayout,QLabel,QHBoxLayout,QDialog,QWidget, QVBoxLayout, QTextEdit, QPushButton
#from models.user import User
from repositories.user_repository import get_user_by_username,get_all_users,create_user,delete_user_by_username

"""
Саш, попроси гпт написать это окно, я заебался немного 
и хочу смотреть на тебя, а не в экран компьютера
прости, что не успел закончить всё
нужно сделать ещё заполнение отчётов
я очень тебя люблю и скучаю
мы скоро встретимся, целую
"""

class UserView(QDialog):
    def __init__(self,parent = None, user=None):
        super().__init__(parent)
        '''
        if user is None:
            raise ValueError("Пользователь не передан")

        if not isinstance(user, User):
            print(user)
            raise TypeError(f"Ожидается объект User, получен {type(user)}")
        '''
        self.setWindowTitle("Редактирование пользователей")
        self.setGeometry(100, 60, 700, 500)
        self.user = user

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Таблица пользователей
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Имя пользователя", "Пароль", "Роль", "Активность"])
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        layout.addWidget(self.table)
        self.load_users()

        # Форма для добавления/редактирования пользователя
        form_layout = QHBoxLayout()
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Логин")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Пароль")
        self.input_role = QComboBox()
        self.input_role.addItems(["admin", "warehouse_manager", "production_manager", "logistics"])
        self.input_active = QComboBox()
        self.input_active.addItems(["активен", "не активен"])

        form_layout.addWidget(QLabel("Логин:"))
        form_layout.addWidget(self.input_username)
        form_layout.addWidget(QLabel("Пароль:"))
        form_layout.addWidget(self.input_password)
        form_layout.addWidget(QLabel("Роль:"))
        form_layout.addWidget(self.input_role)
        form_layout.addWidget(QLabel("Активность:"))
        form_layout.addWidget(self.input_active)

        layout.addLayout(form_layout)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Добавить пользователя")
        self.btn_edit = QPushButton("Изменить пользователя")
        self.btn_delete = QPushButton("Удалить пользователя")

        self.btn_add.clicked.connect(self.add_user)
        self.btn_edit.clicked.connect(self.edit_user)
        self.btn_delete.clicked.connect(self.delete_user)

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.table.cellClicked.connect(self.fill_form_from_table)

    def load_users(self):
        from repositories.user_repository import get_all_users
        users = get_all_users()
        self.table.setRowCount(len(users))
        for row, user in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(user.username))
            self.table.setItem(row, 1, QTableWidgetItem(user.password))
            self.table.setItem(row, 2, QTableWidgetItem(user.role))
            self.table.setItem(row, 3, QTableWidgetItem("активен" if getattr(user, "is_active", True) else "не активен"))
    def fill_form_from_table(self, row, column):
        self.input_username.setText(self.table.item(row, 0).text())
        self.input_password.setText(self.table.item(row, 1).text())
        role = self.table.item(row, 2).text()
        active = self.table.item(row, 3).text()
        self.input_role.setCurrentText(role)
        self.input_active.setCurrentText(active)

    def add_user(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()
        role = self.input_role.currentText()
        is_active = self.input_active.currentText() == "активен"
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Логин и пароль обязательны")
            return
        try:
            user = create_user(username, password, username, role)  # full_name = username (или добавить поле)
            # Если есть поле is_active в модели User, обновить его отдельно
            if hasattr(user, "is_active"):
                user.is_active = is_active
            QMessageBox.information(self, "Успех", f"Пользователь {username} добавлен")
            self.load_users()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить пользователя:\n{e}")

    def edit_user(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()
        role = self.input_role.currentText()
        is_active = self.input_active.currentText() == "активен"
        if not username:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для редактирования")
            return
        from repositories.user_repository import update_user_by_username
        try:
            update_user_by_username(username, password=password, role=role, is_active=is_active)
            QMessageBox.information(self, "Успех", f"Пользователь {username} обновлен")
            self.load_users()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить пользователя:\n{e}")

    def delete_user(self):
        username = self.input_username.text().strip()
        if not username:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для удаления")
            return
        reply = QMessageBox.question(self, "Подтверждение", f"Удалить пользователя {username}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if delete_user_by_username(username):
                    QMessageBox.information(self, "Успех", f"Пользователь {username} удалён")
                    self.load_users()
                else:
                    QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить пользователя:\n{e}")