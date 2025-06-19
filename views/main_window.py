from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMenuBar, QMenu, QHBoxLayout
)


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle(f"ИС управления производством ( {user.full_name} )")
        self.setGeometry(450, 300, 500, 250)
        self.user = user
        self.init_ui()

    def init_ui(self):
        # Меню
        '''
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Файл")
        exit_action = file_menu.addAction("Выход")
        exit_action.triggered.connect(self.close)
        '''
        # Основной контент
        central_widget = QWidget()
        layout = QVBoxLayout()

        title_label = QLabel("Добро пожаловать в систему управления производством")
        layout.addWidget(title_label)

        # Кнопки навигации
        btn_layout = QVBoxLayout()

        self.btn_movement_orders = QPushButton("Заказы перемещения")
        self.btn_movement_orders.clicked.connect(self.open_movement_orders_view)
        btn_layout.addWidget(self.btn_movement_orders)

        self.btn_warehouse_management = QPushButton("Управление складами")
        self.btn_warehouse_management.clicked.connect(self.open_warehouse_management_view)
        btn_layout.addWidget(self.btn_warehouse_management)

        self.btn_route_management = QPushButton("Управление маршрутами")
        self.btn_route_management.clicked.connect(self.open_route_management_view)
        btn_layout.addWidget(self.btn_route_management)

        self.btn_documents = QPushButton("Отчеты по действиям с материальными запасами")
        self.btn_documents.clicked.connect(self.open_documents_view)
        btn_layout.addWidget(self.btn_documents)

        self.btn_user_management = QPushButton("Управление пользователями")
        self.btn_user_management.clicked.connect(self.open_user_management_view)
        btn_layout.addWidget(self.btn_user_management)

        layout.addLayout(btn_layout)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_movement_orders_view(self):
        from views.orders.movement_orders_view import OrderView
        self.movement_orders_view = OrderView(parent=self, user=self.user)
        self.movement_orders_view.show()

    def open_warehouse_management_view(self):
        from views.warehouses.warehouse_management_view import WarehouseView
        self.warehouse_management_view = WarehouseView(self)
        self.warehouse_management_view.show()

    def open_route_management_view(self):
        from views.routes.route_management_view import RouteView
        self.route_management_view = RouteView(self)
        self.route_management_view.show()

    def open_documents_view(self):
        from views.documents.documents_view import DocumentView
        self.documents_view = DocumentView(self)
        self.documents_view.show()

    def open_user_management_view(self):
        from views.users.user_management_view import UserView
        self.user_management_view = UserView(parent = self, user=self.user)
        self.user_management_view.show()

