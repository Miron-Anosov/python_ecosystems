DB_PATH = 'rooms.db'

SELECT_BASE = """
    SELECT
        *
    FROM
        `room`
"""

SELECT_ALL_FREE_ROOMS = """
    SELECT
        `room`.id_room,
        `room`.floor,
        `room`.guest,
        `room`.beds,
        `room`.price
    FROM
        `room`
    LEFT JOIN
        `booking` ON
        `room`.id_room = `booking`.id_room
    WHERE `booking`.id_room IS NULL
"""
SELECT_BOOKING = """
                SELECT 
                    *
                FROM 
                    `booking`
                WHERE `booking`.id_room = ?
                
"""

INSERT_ROOM = """
            INSERT INTO `room`(
                                floor,
                                guest, 
                                beds, 
                                price
                                )
                                VALUES( ?, ?, ?, ?
           );
"""

INSET_GUEST = """
            INSERT INTO `booking`(
                                    id_room,
                                    firstName,
                                    lastName,
                                    check_out,
                                    check_in
            
            )
            VALUES( ?, ?, ?, ?, ? )
"""

CREATE_DB = """
            CREATE TABLE IF NOT EXISTS `booking`(
                id_booking INTEGER PRIMARY KEY AUTOINCREMENT,
                id_room INTEGER NOT NULL,
                firstName VARCHAR(255) NOT NULL,
                lastName VARCHAR(255) NOT NULL,
                check_out VARCHAR(255) NOT NULL,
                check_in VARCHAR(255) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS `room` (
                id_room INTEGER PRIMARY KEY AUTOINCREMENT,
                floor INTEGER NOT NULL,
                guest INTEGER NOT NULL,
                beds INTEGER NOT NULL,
                price INTEGER NOT NULL
            );
"""
