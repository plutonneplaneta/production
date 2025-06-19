# main.py

import sys
from PyQt6.QtWidgets import QApplication
from config.database import Base, engine
from views.login.login_window import LoginWindow


def initialize_database():
    """Инициализация базы данных (создание таблиц)"""
    try:
        Base.metadata.create_all(bind=engine)
        print("База данных успешно инициализирована.")
    except Exception as e:
        print(f"Ошибка инициализации БД: {e}")
        sys.exit(1)


def main():
    # Инициализация БД
    initialize_database()

    # Запуск GUI
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()