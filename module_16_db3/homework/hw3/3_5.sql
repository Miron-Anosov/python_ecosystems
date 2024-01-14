SELECT
Battles.name
FROM Battles
WHERE EXISTS(
SELECT
1
FROM Ships
JOIN Outcomes ON
Outcomes.ship = Ships.name
WHERE
Ships.class = 'Kongo'
AND Outcomes.battle = Battles.name)
