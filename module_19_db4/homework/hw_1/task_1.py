import sqlite3

with sqlite3.connect('../../homework.db') as conn:
    cur = conn.cursor()
    cur.execute(
        """                                                              
    SELECT 
        teachers.full_name
    FROM 
        teachers
    JOIN 
        assignments 
    ON 
        assignments.teacher_id = teachers.teacher_id
    JOIN 
        assignments_grades 
    ON 
        assignments_grades.assisgnment_id =  assignments.assisgnment_id
    GROUP BY 
        teachers.full_name
    ORDER BY 
        AVG(assignments_grades.grade)
    LIMIT 1;
    """
    )

