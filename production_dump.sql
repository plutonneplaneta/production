CREATE database `production`;

DROP TABLE IF EXISTS `production`.`Users`;
CREATE TABLE `production`.`Users` (
  `user_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(50) UNIQUE NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `full_name` VARCHAR(100) NOT NULL,
  `role` ENUM("admin", "warehouse_manager", "production_manager", "logistics"),
  `is_active` BOOLEAN DEFAULT TRUE,
  `last_login` TIMESTAMP
);

DROP TABLE IF EXISTS `production`.`Warehouses`;
CREATE TABLE `production`.`Warehouses` (
  `warehouse_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) UNIQUE NOT NULL,
  `type` ENUM('production', 'transit', 'finished_products') NOT NULL,
  `location` VARCHAR(255),
  `is_active` BOOLEAN DEFAULT TRUE,
  `description` TEXT
);

DROP TABLE IF EXISTS `production`.`Materials`;
CREATE TABLE `production`.`Materials` (
  `material_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `code` VARCHAR(50) UNIQUE NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `type` ENUM('raw', 'material', 'semi_finished', 'finished') NOT NULL,
  `unit` VARCHAR(20) NOT NULL,
  `min_stock_level` DECIMAL(12, 3),
  `max_stock_level` DECIMAL(12, 3),
  `production_status` ENUM('in_progress', 'decommissioned', 'released') NOT NULL,
  `description` TEXT
);

DROP TABLE IF EXISTS `production`.`StockBalances`;
CREATE TABLE `production`.`StockBalances` (
  `balance_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `warehouse_id` INT NOT NULL,
  `material_id` INT NOT NULL,
  `quantity` DECIMAL(12, 3) NOT NULL,
  `last_update` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id) ON DELETE RESTRICT,
   FOREIGN KEY (material_id) REFERENCES Materials(material_id) ON DELETE RESTRICT,
   UNIQUE (warehouse_id, material_id)
);

DROP TABLE IF EXISTS `production`.`TransferRoutes`;
CREATE TABLE `production`.`TransferRoutes` (
  `route_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `from_warehouse_id` INT NOT NULL,
  `to_warehouse_id` INT NOT NULL,
  `transit_warehouse_id` INT,
  `transport_method` VARCHAR(50),
  `duration_hours` INT NOT NULL,
  `reliability_rating` DECIMAL(3, 2) DEFAULT 5.00 CHECK (reliability_rating BETWEEN 1.00 AND 10.00),
  `is_active` BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (from_warehouse_id) REFERENCES Warehouses(warehouse_id) ON DELETE RESTRICT,
  FOREIGN KEY (to_warehouse_id) REFERENCES Warehouses(warehouse_id) ON DELETE RESTRICT,
  FOREIGN KEY (transit_warehouse_id) REFERENCES Warehouses(warehouse_id) ON DELETE RESTRICT
);

DROP TABLE IF EXISTS `production`.`TransferOrders`;
CREATE TABLE `production`.`TransferOrders` (
  `order_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
  `route_id` INT,
  `shipment_date` DATE COMMENT 'фактическая дата отправления',
  `arrival_date` DATE COMMENT 'фактическая дата прибытия',
  `status` ENUM('created', 'in_progress', 'completed', 'cancelled') DEFAULT 'created',
  `created_by` INT NOT NULL COMMENT 'пользователь,  создавший запись',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (route_id) REFERENCES TransferRoutes(route_id) ON DELETE SET NULL,
  FOREIGN KEY (created_by) REFERENCES Users(user_id) ON DELETE RESTRICT
);

DROP TABLE IF EXISTS `production`.`OrderFilling`;
CREATE TABLE `production`.`OrderFilling` (
  `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `material_id` INT NOT NULL,
  `quantity` DECIMAL(12, 3) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES TransferOrders(order_id) ON DELETE RESTRICT,
  FOREIGN KEY (material_id) REFERENCES Materials(material_id) ON DELETE RESTRICT
);

DROP TABLE IF EXISTS `production`.`TransferLosses`;
CREATE TABLE `production`.`TransferLosses` (
  `loss_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `route_id` INT NOT NULL,
  `material_id` INT NOT NULL,
  `expected_quantity` DECIMAL(12, 3) NOT NULL,
  `actual_quantity` DECIMAL(12, 3) NOT NULL,
  `loss_percentage` DECIMAL(5, 2) GENERATED ALWAYS AS ((expected_quantity - actual_quantity) / expected_quantity * 100) STORED,
  `loss_reason` VARCHAR(255),
  `recorded_date` DATE NOT NULL,
  `recorded_by` INT NOT NULL,
  FOREIGN KEY (order_id) REFERENCES TransferOrders(order_id) ON DELETE RESTRICT,
  FOREIGN KEY (route_id) REFERENCES TransferRoutes(route_id) ON DELETE RESTRICT,
  FOREIGN KEY (material_id) REFERENCES Materials(material_id) ON DELETE RESTRICT,
  FOREIGN KEY (recorded_by) REFERENCES Users(user_id) ON DELETE RESTRICT
);

DROP TABLE IF EXISTS `production`.`Shipments`;
CREATE TABLE `production`.`Shipments` (
  `shipment_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `document_number` VARCHAR(50) UNIQUE NOT NULL,
  `shipment_date` DATE NOT NULL,
  `shipped_by` INT NOT NULL,
  `warehouse_id` INT NOT NULL,
  `status` ENUM("draft", "confirmed", "cancelled") DEFAULT "draft",
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `created_by` INT NOT NULL,
  FOREIGN KEY (order_id) REFERENCES TransferOrders(order_id) ON DELETE RESTRICT,
  FOREIGN KEY (shipped_by) REFERENCES Users(user_id) ON DELETE RESTRICT,
  FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id) ON DELETE RESTRICT,
  FOREIGN KEY (created_by) REFERENCES Users(user_id) ON DELETE RESTRICT
);

DROP TABLE IF EXISTS `production`.`Receipts`;
CREATE TABLE `production`.`Receipts` (
  `receipt_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `document_number` VARCHAR(50) UNIQUE NOT NULL,
  `receipt_date` DATE NOT NULL,
  `received_by` INT NOT NULL,
  `warehouse_id` INT NOT NULL,
  `status` ENUM("draft", "confirmed", "cancelled") DEFAULT "draft",
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `created_by` INT NOT NULL,
  FOREIGN KEY (order_id) REFERENCES TransferOrders(order_id) ON DELETE RESTRICT,
  FOREIGN KEY (received_by) REFERENCES Users(user_id) ON DELETE RESTRICT,
  FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id) ON DELETE RESTRICT,
  FOREIGN KEY (created_by) REFERENCES Users(user_id) ON DELETE RESTRICT
);

DROP TABLE IF EXISTS `production`.`DocumentTypes`;
CREATE TABLE `production`.`DocumentTypes` (
  `type_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `type_name` ENUM("create_order", "shipment", "receipt", "writeoff", "production_output") NOT NULL,
  `description` TEXT
);

INSERT INTO `production`.`DocumentTypes` (`type_name`, `description`) VALUES
('create_order', 'Документ создания заказа перемещения'),
('shipment', 'Документ отгрузки'),
('receipt', 'Документ получения'),
('writeoff', 'Документ списания в производство'),
('production_output', 'Документ выпуска готовой продукции');


