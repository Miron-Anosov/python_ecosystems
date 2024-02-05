import sqlite3

with sqlite3.connect('../../homework.db') as conn:
    cur = conn.cursor()
    cur.execute(
        """                                                              
    SELECT 
        students.full_name,
        assignments_grades.grade
    FROM 
        students
    left JOIN 
        assignments_grades
    ON
        assignments_grades.student_id = students.student_id
    GROUP BY 
        students.student_id
    ORDER BY
        assignments_grades.grade DESC
    LIMIT 10;

    """
    )
