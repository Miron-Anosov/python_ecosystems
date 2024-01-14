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
