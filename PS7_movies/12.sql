SELECT title FROM movies WHERE title IN (SELECT title FROM movies WHERE id IN (SELECT movie_id from stars WHERE person_id IN (SELECT id FROM people WHERE name = 'Bradley Cooper' ))) INTERSECT SELECT title FROM movies WHERE title IN (SELECT title FROM movies WHERE id IN (SELECT movie_id from stars WHERE person_id IN (SELECT id FROM people WHERE name = 'Jennifer Lawrence' )));