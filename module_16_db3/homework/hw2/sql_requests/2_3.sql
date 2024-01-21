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