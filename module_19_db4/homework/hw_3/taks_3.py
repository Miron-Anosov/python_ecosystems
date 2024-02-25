import sqlite3

with sqlite3.connect('../../homework.db') as conn:
    cur = conn.cursor()
    cur.execute(
        """     
                                                                 
    SELECT
        students.full_name
    FROM 
        students
    WHERE 
        students.student_id 
        IN (
    
                SELECT
                    assignments_grades.student_id
                FROM 
                    assignments_grades
                JOIN	-- Тот самый единственный join по тз. Для чего такие ограничения в практическом применении?
                    assignments
                ON 
                    assignments.assisgnment_id = assignments_grades.assisgnment_id
                GROUP BY assignments.teacher_id
                ORDER BY AVG(assignments_grades.grade) DESC;
            )

    """
    )
