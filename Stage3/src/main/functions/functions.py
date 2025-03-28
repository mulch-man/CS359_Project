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
# 2. Count the number of classes available at each gym facility (Placeholder)
def countClassesPerGym():
    pass

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
# 4. List all equipment of a specific type (Placeholder)
def listEquipmentByType(equipmentType):
    pass

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
# 6. Get the list of classes taught by a specific instructor (Placeholder)
def getClassesByInstructor(instructorId):
    pass

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
    pass

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
    pass
