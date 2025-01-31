
-- Get all competitors with their rank and points

SELECT DISTINCT c.name, r.rank, r.points
FROM competitors_table c
JOIN competitor_rankings_table r ON c.competitor_id = r.competitor_id

-- Find competitors ranked in the top 5

SELECT c.competitor_id, c.name, c.country, c.country_code, c.abbreviation, r.rank, r.points
FROM competitors_table c
JOIN competitor_rankings_table r ON c.competitor_id = r.competitor_id
WHERE r.rank <= 5
ORDER BY r.rank
-- List competitors with no rank movement (stable rank)

SELECT c.competitor_id, c.name, c.country, c.country_code, c.abbreviation, r.rank, r.movement, r.points
FROM competitors_table c
JOIN competitor_rankings_table r ON c.competitor_id = r.competitor_id
WHERE r.movement = 0

-- Get the total points of competitors from a specific country (e.g., Croatia)

SELECT c.country, SUM(r.points) AS total_points
FROM competitors_table c
JOIN competitor_rankings_table r ON c.competitor_id = r.competitor_id
WHERE c.country = 'Croatia'
GROUP BY c.country

-- Count the number of competitors per country

SELECT c.country, COUNT(c.competitor_id) AS competitor_count
FROM competitors_table c
GROUP BY c.country
ORDER BY competitor_count DESC;

-- Find competitors with the highest points in the current week
----Week already excluded
