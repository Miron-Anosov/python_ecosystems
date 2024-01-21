# TASK_1 = '"Вся информацию о каждом заказе:"'
# TASK_2 = 'Имена покупателей, которые не сделали ни одного заказа:'
# TASK_3 = 'Номера заказа, имена продавца и покупателя, если место жительства продавца и покупателя не совпадают:'
# TASK_4 = 'Для покупателей, которые сделали заказ напрямую (без помощи менеджеров), выведите имена и номера заказов:'
# TASK_5 = 'Выведите имена уникальных пар покупателей, живущих в одном городе и имеющих одного менеджера'

TASK_5_UNIQUE_CUSTOMER = """
        DROP VIEW IF EXISTS `unique_customer`;
        CREATE VIEW `unique_customer` AS
        SELECT 
            `customer`.full_name AS name_customer,
            cus.full_name AS customer_name,
            `manager`.full_name AS manager
        FROM 
             `order`
        JOIN `manager` ON
            `manager`.manager_id = `order`.manager_id
        JOIN
            `customer` ON
            `customer`.customer_id = `order`.customer_id
        JOIN
            `customer` AS cus ON 
            `customer`.city = cus.city
        WHERE 
            cus.manager_id = `customer`.manager_id
            AND
            cus.customer_id != `customer`.customer_id
            AND
            cus.city = `customer`.city;
"""

TASK_4_ORDER_WITHOUT_MANAGER = """
        DROP VIEW IF EXISTS `order_without_manager`;
        CREATE VIEW `order_without_manager` AS
        SELECT
            `customer`.full_name AS customer,
            `order`.order_no AS order_number
        FROM 
            `order`
        LEFT JOIN `manager` ON
            `manager`.manager_id = `order`.manager_id
        JOIN
            `customer` ON
            `customer`.customer_id = `order`.customer_id
        WHERE 
            `order`.manager_id is NULL;
"""

TASK_3_ORDER_DIFFERENT_CITY = """
        DROP VIEW IF EXISTS `order_different_city`;
        CREATE VIEW `order_different_city` AS
        SELECT
            `order`.order_no AS order_number,
            `manager`.full_name AS manager,
            `customer`.full_name AS customer
        FROM 
            `order`
        JOIN 
            `manager` ON
            `manager`.manager_id = `order`.manager_id
        JOIN
            `customer` ON
            `customer`.customer_id = `order`.customer_id
        WHERE
            `manager`.city != `customer`.city;
"""

TASK_2_CUSTOMER_WITHOUT_ORDER = """
        DROP VIEW IF EXISTS `customer_without_order`;
        CREATE VIEW IF NOT EXISTS `customer_without_order` AS
        SELECT
            `customer`.full_name AS customer
        FROM 
             `customer`
        LEFT JOIN 
            `order` ON 
            `customer`.customer_id = `order`.customer_id
        WHERE 
            `order`.customer_id is NULL;
"""

TASK_1_ALL_INFO_ABOUT_ORDER = """
        DROP VIEW IF EXISTS `all_info_about_order`;
        CREATE VIEW IF NOT EXISTS `all_info_about_order` AS
        SELECT
            `customer`.full_name AS customer,
            `manager`.full_name AS manager,
            `order`.purchase_amount AS sum_order,
            `order`.`date` AS `date`
        FROM  
            `order`
        JOIN `customer` ON 
            `customer`.customer_id = `order`.customer_id
        JOIN `manager` ON 
            `manager`.manager_id = `order`.manager_id;
"""

requests_sql_data = (TASK_1_ALL_INFO_ABOUT_ORDER,
                     TASK_2_CUSTOMER_WITHOUT_ORDER,
                     TASK_3_ORDER_DIFFERENT_CITY,
                     TASK_4_ORDER_WITHOUT_MANAGER,
                     TASK_5_UNIQUE_CUSTOMER
                     )
