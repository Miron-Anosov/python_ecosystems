SELECT
Outcomes.ship AS name
FROM Classes
JOIN Outcomes ON
Outcomes.ship = Classes.class

UNION
SELECT
Ships.name  AS name
FROM Classes
JOIN Ships ON
Ships.name = Classes.class
