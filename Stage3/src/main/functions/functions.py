import sqlite3

from main.database import connectDatabase


#--------------------------------------------------------------------------------------------------------------------
# 1. Retrieve a list of all members in the gym
def getAllMembers():
    connection = connectDatabase()
    if connection:
        cursor = connection.cursor()
        try:
            # Updated query: join through Payment to get the membership plan information
            cursor.execute("""
                SELECT M.name, M.email, M.age, MP.planType 
                FROM Member M
                LEFT JOIN Payment P ON M.memberId = P.memberId
                LEFT JOIN MembershipPlan MP ON P.planId = MP.planId
            """)
            members = cursor.fetchall()
            print("Name | Email | Age | Membership Plan")
            print("-" * 50)
            if members:
                for member in members:
                    print(f"{member[0]} | {member[1]} | {member[2]} | {member[3]}")
            else:
                print("No members found.")
        except sqlite3.Error as error:
            print('Error fetching members - ', error)
        finally:
            connection.close()

#--------------------------------------------------------------------------------------------------------------------
# 2. Count the number of classes available at each gym facility
def countClassesPerGym():
    connection = connectDatabase()
    if connection:
        cursor = connection.cursor()
        try:
            # Updated query: join through Payment to get the membership plan information
            cursor.execute("""
                SELECT location, count(gymId)
                FROM GymFacility NATURAL JOIN Class
                GROUP BY gymId
            """)
            output = cursor.fetchall()

            print("-" * 50)
            for row in output:
                print(f"Classes available at {row[0]}: {row[1]}")
        except sqlite3.Error as error:
            print('Error fetching classes per gym facility - ', error)
        finally:
            connection.close()

#--------------------------------------------------------------------------------------------------------------------
# 3. Retrieve the names of members attending a specific class
def getMembersByClass(classId):
    connection = connectDatabase()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT Member.name FROM Member 
                JOIN Attends ON Member.memberId = Attends.memberId 
                WHERE Attends.classId = ?
            """, (classId,))
            members = cursor.fetchall()
            if members:
                print(f"Members attending Class ID {classId}:")
                for member in members:
                    print(member[0])
            else:
                print("No members found for the given class.")
        except sqlite3.Error as error:
            print('Error fetching members by class - ', error)
        finally:
            connection.close()

#--------------------------------------------------------------------------------------------------------------------
# 4. List all equipment of a specific type
def listEquipmentByType(equipmentType):
    connection = connectDatabase()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""SELECT name
                   FROM Equipment
                   WHERE type = '{equipmentType}'""")
            output = cursor.fetchall()
            if output:
                print(f"-- Equipment of type {equipmentType}: " + "-" * 50)
                for row in output:
                    print(row[0])
            else:
                print("No equipment found for the given type.")
        except sqlite3.Error as error:
            print('Error fetching equipment by type - ', error)
        finally:
            connection.close()

#--------------------------------------------------------------------------------------------------------------------
# 5. Find all members with expired memberships
def getExpiredMemberships():
    connection = connectDatabase()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT name FROM Member 
                WHERE membershipEndDate < DATE('now')
            """)
            expired_members = cursor.fetchall()
            if expired_members:
                print("Expired Memberships:")
                for member in expired_members:
                    print(member[0])
            else:
                print("No expired memberships found.")
        except sqlite3.Error as error:
            print('Error fetching expired memberships - ', error)
        finally:
            connection.close()

#--------------------------------------------------------------------------------------------------------------------
# 6. Get the list of classes taught by a specific instructor
def getClassesByInstructor(instructorId):
    connection = connectDatabase()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""SELECT className, classType, duration, classCapacity, name, phone
                    FROM Class NATURAL JOIN Instructor
                    WHERE instructorId = '{instructorId}'""")
            output = cursor.fetchall()

            if output:
                print(f"-- Classes Taught by {output[0][4]}: " + "-" * 65)
                print(f"-- Phone: {output[0][5]}")
                for row in output:
                    print(f"Class: {row[0]}, Type: {row[1]}, Duration: {row[2]}, Capacity: {row[3]}")
            else:
                print("No taught classes found by given instructor.")

        except sqlite3.Error as error:
            print('Error fetching classes taught by given instructor - ', error)
        finally:
            connection.close()

#--------------------------------------------------------------------------------------------------------------------
# 7. Calculate the average age of members with active and expired memberships
def calculateAverageAge():
    connection = connectDatabase()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT AVG(CASE WHEN membershipEndDate >= DATE('now') THEN age ELSE NULL END) AS active_avg,
                       AVG(CASE WHEN membershipEndDate < DATE('now') THEN age ELSE NULL END) AS expired_avg
                FROM Member
            """)
            result = cursor.fetchone()
            print(f"Average Age of Active Members: {result[0]:.2f}")
            print(f"Average Age of Expired Members: {result[1]:.2f}")
        except sqlite3.Error as error:
            print('Error calculating average age - ', error)
        finally:
            connection.close()

#--------------------------------------------------------------------------------------------------------------------
# 8. Find the top three instructors who teach the most classes (Placeholder)
def topInstructors():
    connection = connectDatabase()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""SELECT name, COUNT(classId)
                            FROM Instructor NATURAL JOIN Class
                            GROUP BY instructorId
                            ORDER BY COUNT(classId) DESC
                            LIMIT 3
                            """)
            output = cursor.fetchall()

            if output:
                print("-- Top-Teaching Instructors: " + "-" * 50)
                for row in output:
                    print(f"{row[0]} | Teaches: {row[1]}")
                print("-" * 79)
            else:
                print("No results.")

        except sqlite3.Error as error:
            print('Error fetching top-teaching instructors - ', error)
        finally:
            connection.close()

#--------------------------------------------------------------------------------------------------------------------
# 9. Find the members who have attended all classes of a specific type
def findMembersByClassType(classType):
    connection = connectDatabase()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT M.name FROM Member M
                WHERE NOT EXISTS (
                    SELECT C.classId FROM Class C
                    WHERE C.classType = ? AND NOT EXISTS (
                        SELECT A.classId FROM Attends A
                        WHERE A.memberId = M.memberId AND A.classId = C.classId
                    )
                )
            """, (classType,))
            members = cursor.fetchall()
            if members:
                print(f"Members who attended all {classType} classes:")
                for member in members:
                    print(member[0])
            else:
                print(f"No members have attended all {classType} classes.")
        except sqlite3.Error as error:
            print('Error fetching members by class type - ', error)
        finally:
            connection.close()

#--------------------------------------------------------------------------------------------------------------------
# 10. Get all members who attended classes in the last month (Placeholder)
def recentClassAttendance():
    connection = connectDatabase()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""WITH Recents AS (
                                SELECT *
                                FROM Attends
                                WHERE attendanceDate > DATE('now', '-1 month') ),
                            Counts AS (
                                SELECT memberId, Count(classId) AS classCount
                                FROM Attends
                                GROUP BY memberId )
                            SELECT name, classCount, className, classType
                            FROM Member NATURAL JOIN Recents
                            NATURAL JOIN Class NATURAL JOIN Counts
                            """)
            output = cursor.fetchall()

            if output:
                print("-- Recent Class Attendees: " + "-" * 110)
                print(f"{'Member Name':<25} {'Total Classes Attended':<30} {'Classes Attended':<45} {'Class Types'}")
                print("=" * 137)

                # lord forgive me for this logic i have created
                info = [""] * 4
                for row in output:
                    if info[0] != row[0]:
                        if info[0] != "":
                            print(f"{info[0]:<35} {info[1]:<20} {info[2]:<45} {info[3]}")
                        info[0] = row[0]
                        info[1] = row[1]
                        info[2] = ""
                        info[3] = ""
                    info[2] += row[2] + ', '
                    info[3] += row[3] + ", "
                # To print the last row
                print(f"{info[0]:<35} {info[1]:<20} {info[2]:<45} {info[3]}")

                print("-" * 137)
            else:
                print("No recent class attendees.")

        except sqlite3.Error as error:
            print('Error fetching classes recent class attendees - ', error)
        finally:
            connection.close()