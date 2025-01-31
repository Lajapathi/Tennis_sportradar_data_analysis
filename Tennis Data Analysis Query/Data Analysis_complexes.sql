
-- List all venues along with their associated complex name

SELECT v.venue_name, v.city_name, v.country_name, c.complex_name
FROM venues_table v
JOIN complexes_table c ON v.complex_id = c.complex_id

-- Count the number of venues in each complex

SELECT c.complex_name, COUNT(v.venue_id) AS venue_count
FROM venues_table v
JOIN complexes_table c ON v.complex_id = c.complex_id
GROUP BY c.complex_name

-- Get details of venues in a specific country (e.g., Chile)

SELECT v.venue_id, v.venue_name, v.city_name, v.country_name, v.country_code, v.timezone, c.complex_name
FROM venues_table v
JOIN complexes_table c ON v.complex_id = c.complex_id
WHERE v.country_name = 'Chile';

-- Identify all venues and their timezones

SELECT v.venue_name, v.city_name, v.country_name, v.timezone
FROM venues_table v

-- Find complexes that have more than one venue

SELECT c.complex_name, COUNT(v.venue_id) AS venue_count
FROM venues_table v
JOIN complexes_table c ON v.complex_id = c.complex_id
GROUP BY c.complex_name
HAVING COUNT(v.venue_id) > 1

-- List venues grouped by country

SELECT v.country_name, v.venue_name
FROM venues_table v
GROUP BY v.country_name,v.venue_name
ORDER BY country_name ASC

-- Find all venues for a specific complex (e.g., Nacional)

SELECT v.venue_id, v.venue_name, v.city_name, v.country_name, v.country_code, v.timezone
FROM venues_table v
JOIN complexes_table c ON v.complex_id = c.complex_id
WHERE c.complex_name = 'Spo1 Park'
