import sqlite3

with sqlite3.connect('../../homework.db') as conn:
    cur = conn.cursor()
    cur.execute(
        """                                                              
    SELECT  
        MAX(total_late) as max_late,
        AVG( total_late) AS middle_late,
        MIN(total_late)AS min_late
    FROM(
        SELECT 
            group_id,
            SUM(due_date < `date`) AS total_late
        FROM 
            assignments as ass
        JOIN 
            assignments_grades as ag
        ON
            ass.assisgnment_id = ag.assisgnment_id
        GROUP BY group_id
                )
    AS strange_task
"""
    )
