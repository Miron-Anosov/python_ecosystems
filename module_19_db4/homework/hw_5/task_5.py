import sqlite3


with sqlite3.connect('../../homework.db') as conn:
    cur = conn.cursor()
    cur.execute(
        """                                                              
    SELECT
        students_groups.group_id,
        COUNT(students.student_id) AS students_in_the_group,
        ROUND(AVG(assignments_grades.grade),2) AS avg_grate,
        COUNT(CASE WHEN assignments_grades.grade IS NULL THEN 1 END) AS not_submit_a_job,
        COUNT(CASE WHEN assignments_grades.date > assignments.due_date THEN 1 END) AS late_sub,
        COUNT(
            DISTINCT CASE
                WHEN (
                    SELECT COUNT(*)
                    FROM assignments_grades AS ag2
                    WHERE ag2.student_id = students.student_id AND ag2.grade IS NOT NULL
                ) > 1 THEN students.student_id
            END
        ) AS repeated_sub
    FROM 
        students_groups
    LEFT JOIN 
        students 
        ON students_groups.group_id = students.group_id
    LEFT JOIN 
        assignments_grades 
        ON students.student_id = assignments_grades.student_id
    LEFT JOIN 
        assignments 
        ON assignments_grades.assisgnment_id = assignments.assisgnment_id
    GROUP BY students.group_id
    """
    )
