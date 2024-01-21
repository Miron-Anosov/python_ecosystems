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
