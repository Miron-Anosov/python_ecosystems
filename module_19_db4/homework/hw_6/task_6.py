import sqlite3


with sqlite3.connect('../../homework.db') as conn:
    cur = conn.cursor()
    cur.execute(
        """                                                              
    SELECT
    AVG(assignments_grades.grade) AS avg_grage
    FROM 
        assignments_grades
    JOIN 
        assignments
    ON assignments.assisgnment_id = assignments_grades.assisgnment_id
    WHERE 
        assignments.assignment_text LIkE 'прочитать%' OR assignments.assignment_text LIKE 'выучить%';
    """
    )
