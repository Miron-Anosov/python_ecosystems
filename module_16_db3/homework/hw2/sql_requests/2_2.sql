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
