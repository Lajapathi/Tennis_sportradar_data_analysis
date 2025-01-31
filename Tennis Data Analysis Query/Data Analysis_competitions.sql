
-- List all competitions along with their category name

SELECT DISTINCT c.competition_name, c.type, c.gender, ct.category_name
FROM competitions_table c
INNER JOIN categories_table ct ON c.category_id = ct.category_id

-- Count the number of competitions in each category

SELECT ct.category_name, COUNT(c.competition_id) AS competition_count
FROM competitions_table c
JOIN categories_table ct ON c.category_id = ct.category_id
GROUP BY ct.category_name 

-- Find all competitions of type 'doubles'

SELECT c.competition_id, c.competition_name, c.type, c.gender, ct.category_name
FROM competitions_table c
JOIN categories_table ct ON c.category_id = ct.category_id
WHERE c.type = 'doubles'

-- Get competitions that belong to a specific category (e.g., ITF Men)

SELECT c.competition_id, c.competition_name, c.type, c.gender
FROM competitions_table c
JOIN categories_table ct ON c.category_id = ct.category_id
WHERE ct.category_name = 'ITF Men'

-- Identify parent competitions and their sub-competitions

SELECT p.competition_id AS parent_competition_id, p.competition_name AS parent_competition_name, s.competition_id AS sub_competition_id, s.competition_name AS sub_competition_name
FROM competitions_table p
LEFT JOIN competitions_table s ON p.competition_id = s.parent_id
WHERE p.parent_id ='NULL'

-- Analyze the distribution of competition types by category

SELECT ct.category_name, c.type,c.gender, COUNT(c.competition_id) AS competition_count
FROM competitions_table c
JOIN categories_table ct ON c.category_id = ct.category_id
GROUP BY ct.category_name, c.type, c.gender
ORDER BY ct.category_name, c.type, c.gender
--------
SELECT ct.category_name, c.type, COUNT(c.competition_id) AS competition_count
FROM competitions_table c
JOIN categories_table ct ON c.category_id = ct.category_id
GROUP BY ct.category_name, c.type
ORDER BY ct.category_name, c.type

-- List all competitions with no parent (top-level competitions)

SELECT c.competition_id, c.competition_name, c.type, c.gender, ct.category_name
FROM competitions_table c
JOIN categories_table ct ON c.category_id = ct.category_id
WHERE c.parent_id ='NULL'

