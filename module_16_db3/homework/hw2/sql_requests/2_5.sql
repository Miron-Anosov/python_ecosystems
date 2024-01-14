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
