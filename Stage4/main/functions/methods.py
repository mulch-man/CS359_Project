import sqlite3
from database import connectDatabase

#--------------------------------------------------------------------------------------------------------------------
#   MEMBER OPERATIONS
#--------------------------------------------------------------------------------------------------------------------
def newMember(args=[""]*9):  # args[7] = planId or empty
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            # Insert member
            cursor.execute(f"""
                INSERT INTO Member (name, email, phone, address, age, membershipStartDate, membershipEndDate)
                VALUES ('{args[0]}', '{args[1]}', '{args[2]}', '{args[3]}', {int(args[4])}, '{args[5]}', '{args[6]}');
            """)
            member_id = cursor.lastrowid

            # Optional: Assign plan
            if args[7] != "":
                cursor.execute(f"""
                    INSERT INTO Payment (memberId, planId, amountPaid, paymentDate)
                    VALUES ({member_id}, {int(args[7])}, {int(args[8])}, {args[5]});
                """)
        except sqlite3.Error as error:
            output += f"Error inserting new member - {error}\n"
        finally:
            connection.commit()
            connection.close()
    print(output)

def updateMember(memId=0, args=[""]*9):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                SELECT name, email, phone, address, age, membershipStartDate, membershipEndDate
                FROM Member
                WHERE memberid = {memId};
            """)
            # Intended to fill any missing spaces in argument input with the current values of the tuple being updated
            result = cursor.fetchall()
            for i in range(len(args)):
                if args[i] == "":
                    args[i] = result[0][i]

            cursor.execute(f"""
                UPDATE Member
                SET name = '{args[0]}', email = '{args[1]}', phone = '{args[2]}', address = '{args[3]}',
                    age = {int(args[4])}, membershipStartDate = '{args[5]}', membershipEndDate = '{args[6]}'
                WHERE memberId = {memId};
            """)
            member_id = cursor.lastrowid

            # Optional: Assign plan
            if args[7] != "":
                cursor.execute(f"""
                    INSERT INTO Payment (memberId, planId)
                    VALUES ({member_id}, {int(args[7])});
                """)
        except sqlite3.Error as error:
            output += f"Error updating member information - {error}\n"
        finally:
            connection.commit()
            connection.close()
    print(output)

def delMember(memId=0):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                DELETE FROM Member
                WHERE memberId = {memId};
            """)
        except sqlite3.Error as error:
            output += f"Error deleting member - {error}\n"
        finally:
            connection.commit()
            connection.close()
    print(output)

def getAllMemberships(return_output=False):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                SELECT *
                FROM MembershipPlan;
            """)
            members = cursor.fetchall()
            output += "Plan ID | Plan Type | Cost\n"
            output += "-" * 50 + "\n"
            if members:
                for member in members:
                    output += f"{member[0]} | {member[1]} | {member[2]}\n"
            else:
                output += "No memberships found.\n"
        except sqlite3.Error as error:
            output += f"Error getting membership plans - {error}\n"
        finally:
            connection.commit()
            connection.close()
    return output if return_output else print(output)

#--------------------------------------------------------------------------------------------------------------------
#   CLASS OPERATIONS
#--------------------------------------------------------------------------------------------------------------------
def showClasses(return_output=False):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT *
                FROM Class;
            """)
            classes = cursor.fetchall()
            output += "ID | Name | Type | Duration | Capacity | Instructor ID | Gym ID\n"
            output += "-" * 50 + "\n"
            if classes:
                for aClass in classes:
                    output += f"{aClass[0]} | {aClass[1]} | {aClass[2]} | {aClass[3]} | {aClass[4]} | {aClass[5]} | {aClass[6]}\n"
            else:
                output += "No classes found.\n"
        except sqlite3.Error as error:
            output += f"Error fetching classes - {error}\n"
        finally:
            connection.close()
    return output if return_output else print(output)

def newClass(args=[""]*6):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO Class (className, classType, duration, classCapacity, instructorId, gymId) VALUES
                ('{args[0]}', '{args[1]}', {int(args[2])}, {int(args[3])}, {int(args[4])}, {int(args[5])});
            """)
        except sqlite3.Error as error:
            output += f"Error adding new class - {error}\n"
        finally:
            connection.commit()
            connection.close()
    print(output)

def updateClass(classId=0, args=[""]*6):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                SELECT className, classType, duration, classCapacity, instructorId, gymId
                FROM Class
                WHERE classId = {classId};
            """)
            # Intended to fill any missing spaces in argument input with the current values of the tuple being updated
            result = cursor.fetchall()
            print(result)
            for i in range(len(args)):
                if args[i] == "":
                    args[i] = result[0][i]
            print(args)

            cursor.execute(f"""
                UPDATE Class
                SET className = '{args[0]}', classType = '{args[1]}', duration = {int(args[2])}, classCapacity = {int(args[3])},
                    instructorId = {int(args[4])}, gymId = {int(args[5])}
                WHERE classId = {classId};
            """)
        except sqlite3.Error as error:
            output += f"Error updating class information - {error}\n"
        finally:
            connection.commit()
            connection.close()
    print(output)

def delClass(classId=0):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                DELETE FROM Class
                WHERE classId = {classId};
            """)
        except sqlite3.Error as error:
            output += f"Error deleting class - {error}\n"
        finally:
            connection.commit()
            connection.close()
    print(output)

def checkClassEnrollment(classId=0):
    connection = connectDatabase()
    check = False
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                SELECT *
                FROM Member NATURAL JOIN Attends
                WHERE classId = {classId};
            """)
            output = cursor.fetchall()
            if len(output) > 0:
                check = True
        except sqlite3.Error as error:
            output += f"Error deleting class - {error}\n"
    return check

def moveMembersOfClass(oldId=0, newId=0):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                UPDATE Attends
                SET classId = {newId}
                WHERE classId = {oldId};
            """)
        except sqlite3.Error as error:
            output += f"Error moving class members class - {error}\n"
        finally:
            connection.commit()
            connection.close()
    print(output)

# ----------------------------------------------------------------------------------------------------------------------------
def addClassAttendee(args=[""]*3):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO Attends (memberId, classId, attendanceDate) VALUES
                ({args[0]}, {int(args[1])}, '{args[2]}');
            """)
        except sqlite3.Error as error:
            output += f"Error adding new attendance - {error}\n"
        finally:
            connection.commit()
            connection.close()
    print(output)

def updateClassAttendee(memberId=0, classId=0):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                UPDATE Attends
                SET classId = {classId}
                WHERE memberId = {memberId};
            """)
        except sqlite3.Error as error:
            output += f"Error updating class attendance - {error}\n"
        finally:
            connection.commit()
            connection.close()
    print(output)

def deleteClassAttendee(memberId=0, classId=0):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                DELETE FROM Attends
                WHERE memberId = {memberId} AND classId = {classId};
            """)
        except sqlite3.Error as error:
            output += f"Error deleting class attendance - {error}\n"
        finally:
            connection.commit()
            connection.close()
    print(output)

def showClassAttendance(return_output=False):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT *
                FROM Attends;
            """)
            classes = cursor.fetchall()
            output += "Member's ID | Class ID | Attendance Date\n"
            output += "-" * 50 + "\n"
            if classes:
                for aClass in classes:
                    output += f"{aClass[0]} | {aClass[1]} | {aClass[2]}\n"
            else:
                output += "No attendnace found.\n"
        except sqlite3.Error as error:
            output += f"Error fetching attendnace - {error}\n"
        finally:
            connection.close()
    return output if return_output else print(output)

#--------------------------------------------------------------------------------------------------------------------
#   EQUIPMENT OPERATIONS
#--------------------------------------------------------------------------------------------------------------------
def showEquipment(return_output=False):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT *
                FROM Equipment;
            """)
            classes = cursor.fetchall()
            output += "ID | Name | Type | Quantity | Gym ID\n"
            output += "-" * 50 + "\n"
            if classes:
                for aClass in classes:
                    output += f"{aClass[0]} | {aClass[1]} | {aClass[2]} | {aClass[3]} | {aClass[4]}\n"
            else:
                output += "No equipment found.\n"
        except sqlite3.Error as error:
            output += f"Error fetching equipment - {error}\n"
        finally:
            connection.close()
    return output if return_output else print(output)

def newEquipment(args=[""]*4):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO Equipment (name, type, quantity, gymId) VALUES
                ('{args[0]}', '{args[1]}', {int(args[2])}, {int(args[3])});
            """)
        except sqlite3.Error as error:
            output += f"Error adding new equipment - {error}\n"
        finally:
            connection.commit()
            connection.close()
    print(output)

def updateEquipment(equipmentId=0, args=[""]*4):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                SELECT name, type, quantity, gymId
                FROM Equipment
                WHERE equipmentId = {equipmentId};
            """)
            # Intended to fill any missing spaces in argument input with the current values of the tuple being updated
            result = cursor.fetchall()
            for i in range(len(args)):
                if args[i] == "":
                    args[i] = result[0][i]

            cursor.execute(f"""
                UPDATE Equipment
                SET name = '{args[0]}', type = '{args[1]}', quantity = {int(args[2])}, gymId = {int(args[3])}
                WHERE equipmentId = {equipmentId};
            """)
        except sqlite3.Error as error:
            output += f"Error updating equipment information - {error}\n"
        finally:
            connection.commit()
            connection.close()
    print(output)

def delEquipment(equipmentId=0):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                DELETE FROM Equipment
                WHERE equipmentId = {equipmentId};
            """)
        except sqlite3.Error as error:
            output += f"Error deleting equipment - {error}\n"
        finally:
            connection.commit()
            connection.close()
    print(output)