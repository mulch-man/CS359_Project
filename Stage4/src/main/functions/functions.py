import sqlite3
from database import connectDatabase

#--------------------------------------------------------------------------------------------------------------------
def getAllMembers(return_output=False):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT M.memberId, M.name, M.email, M.age, MP.planType 
                FROM Member M
                LEFT JOIN Payment P ON M.memberId = P.memberId
                LEFT JOIN MembershipPlan MP ON P.planId = MP.planId
            """)
            members = cursor.fetchall()
            output += "ID | Name | Email | Age | Membership Plan\n"
            output += "-" * 70 + "\n"
            if members:
                for member in members:
                    output += f"{member[0]} | {member[1]} | {member[2]} | {member[3]} | {member[4]}\n"
            else:
                output += "No members found.\n"
        except sqlite3.Error as error:
            output += f"Error fetching members - {error}\n"
        finally:
            connection.close()
    return output if return_output else print(output)

#--------------------------------------------------------------------------------------------------------------------
def countClassesPerGym(return_output=False):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT location, count(gymId)
                FROM GymFacility NATURAL JOIN Class
                GROUP BY gymId
            """)
            result = cursor.fetchall()
            output += "-" * 50 + "\n"
            for row in result:
                output += f"Classes available at {row[0]}: {row[1]}\n"
        except sqlite3.Error as error:
            output += f"Error fetching classes per gym facility - {error}\n"
        finally:
            connection.close()
    return output if return_output else print(output)

#--------------------------------------------------------------------------------------------------------------------
def getMembersByClass(classId, return_output=False):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT Member.memberId, Member.name FROM Member 
                JOIN Attends ON Member.memberId = Attends.memberId 
                WHERE Attends.classId = ?
            """, (classId,))
            members = cursor.fetchall()
            if members:
                output += f"Members attending Class ID {classId}:\n"
                for member in members:
                    output += f"ID: {member[0]} | Name: {member[1]}\n"
            else:
                output += "No members found for the given class.\n"
        except sqlite3.Error as error:
            output += f"Error fetching members by class - {error}\n"
        finally:
            connection.close()
    return output if return_output else print(output)

#--------------------------------------------------------------------------------------------------------------------
def listEquipmentByType(equipmentType, return_output=False):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT equipmentId, name FROM Equipment WHERE type = ?", (equipmentType,))
            result = cursor.fetchall()
            if result:
                output += f"-- Equipment of type {equipmentType}:\n" + "-" * 50 + "\n"
                for row in result:
                    output += f"ID: {row[0]} | Name: {row[1]}\n"
            else:
                output += "No equipment found for the given type.\n"
        except sqlite3.Error as error:
            output += f"Error fetching equipment by type - {error}\n"
        finally:
            connection.close()
    return output if return_output else print(output)

#--------------------------------------------------------------------------------------------------------------------
def getExpiredMemberships(return_output=False):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT memberId, name FROM Member WHERE membershipEndDate < DATE('now')")
            result = cursor.fetchall()
            if result:
                output += "Expired Memberships:\n"
                for member in result:
                    output += f"ID: {member[0]} | Name: {member[1]}\n"
            else:
                output += "No expired memberships found.\n"
        except sqlite3.Error as error:
            output += f"Error fetching expired memberships - {error}\n"
        finally:
            connection.close()
    return output if return_output else print(output)

#--------------------------------------------------------------------------------------------------------------------
def getClassesByInstructor(instructorId, return_output=False):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT classId, className, classType, duration, classCapacity, name, phone
                FROM Class NATURAL JOIN Instructor
                WHERE instructorId = ?
            """, (instructorId,))
            result = cursor.fetchall()
            if result:
                output += f"-- Classes Taught by {result[0][5]}:\n" + "-" * 65 + "\n"
                output += f"-- Phone: {result[0][6]}\n"
                for row in result:
                    output += f"ID: {row[0]}, Class: {row[1]}, Type: {row[2]}, Duration: {row[3]}, Capacity: {row[4]}\n"
            else:
                output += "No taught classes found by given instructor.\n"
        except sqlite3.Error as error:
            output += f"Error fetching classes taught by given instructor - {error}\n"
        finally:
            connection.close()
    return output if return_output else print(output)

#--------------------------------------------------------------------------------------------------------------------
def calculateAverageAge(return_output=False):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT 
                    AVG(CASE WHEN membershipEndDate >= DATE('now') THEN age END),
                    AVG(CASE WHEN membershipEndDate < DATE('now') THEN age END)
                FROM Member
            """)
            result = cursor.fetchone()
            active_avg = result[0]
            expired_avg = result[1]

            if active_avg is not None:
                output += f"Average Age of Active Members: {active_avg:.2f}\n"
            else:
                output += "Average Age of Active Members: N/A\n"

            if expired_avg is not None:
                output += f"Average Age of Expired Members: {expired_avg:.2f}\n"
            else:
                output += "Average Age of Expired Members: N/A\n"

        except sqlite3.Error as error:
            output += f"Error calculating average age - {error}\n"
        finally:
            connection.close()
    return output if return_output else print(output)

#--------------------------------------------------------------------------------------------------------------------
def topInstructors(return_output=False):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT instructorId, name, COUNT(classId)
                FROM Instructor NATURAL JOIN Class
                GROUP BY instructorId
                ORDER BY COUNT(classId) DESC
                LIMIT 3
            """)
            result = cursor.fetchall()
            if result:
                output += "-- Top-Teaching Instructors:\n" + "-" * 50 + "\n"
                for row in result:
                    output += f"ID: {row[0]} | Name: {row[1]} | Teaches: {row[2]}\n"
                output += "-" * 79 + "\n"
            else:
                output += "No results.\n"
        except sqlite3.Error as error:
            output += f"Error fetching top-teaching instructors - {error}\n"
        finally:
            connection.close()
    return output if return_output else print(output)

#--------------------------------------------------------------------------------------------------------------------
def findMembersByClassType(classType, return_output=False):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT M.memberId, M.name FROM Member M
                WHERE NOT EXISTS (
                    SELECT C.classId FROM Class C
                    WHERE C.classType = ? AND NOT EXISTS (
                        SELECT A.classId FROM Attends A
                        WHERE A.memberId = M.memberId AND A.classId = C.classId
                    )
                )
            """, (classType,))
            result = cursor.fetchall()
            if result:
                output += f"Members who attended all {classType} classes:\n"
                for member in result:
                    output += f"ID: {member[0]} | Name: {member[1]}\n"
            else:
                output += f"No members have attended all {classType} classes.\n"
        except sqlite3.Error as error:
            output += f"Error fetching members by class type - {error}\n"
        finally:
            connection.close()
    return output if return_output else print(output)

#--------------------------------------------------------------------------------------------------------------------
def recentClassAttendance(return_output=False):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                WITH Recents AS (
                    SELECT * FROM Attends
                    WHERE attendanceDate > DATE('now', '-1 month')
                ),
                Counts AS (
                    SELECT memberId, Count(classId) AS classCount
                    FROM Attends
                    GROUP BY memberId
                )
                SELECT Member.memberId, name, classCount, className, classType
                FROM Member NATURAL JOIN Recents
                NATURAL JOIN Class NATURAL JOIN Counts
            """)
            result = cursor.fetchall()
            if result:
                output += "-- Recent Class Attendees:\n" + "-" * 110 + "\n"
                output += f"{'ID':<5} {'Member Name':<25} {'Total Classes Attended':<30} {'Classes Attended':<45} {'Class Types'}\n"
                output += "=" * 137 + "\n"
                info = ["", "", "", "", ""]
                for row in result:
                    if info[0] != row[0]:
                        if info[0]:
                            output += f"{info[0]:<5} {info[1]:<25} {info[2]:<30} {info[3]:<45} {info[4]}\n"
                        info = [row[0], row[1], row[2], "", ""]
                    info[3] += row[3] + ', '
                    info[4] += row[4] + ', '
                output += f"{info[0]:<5} {info[1]:<25} {info[2]:<30} {info[3]:<45} {info[4]}\n"
                output += "-" * 137 + "\n"
            else:
                output += "No recent class attendees.\n"
        except sqlite3.Error as error:
            output += f"Error fetching classes recent class attendees - {error}\n"
        finally:
            connection.close()
    return output if return_output else print(output)
