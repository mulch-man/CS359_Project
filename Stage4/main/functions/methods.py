import sqlite3
from database import connectDatabase

#--------------------------------------------------------------------------------------------------------------------
#   MEMBER OPERATIONS
#--------------------------------------------------------------------------------------------------------------------
def getLowestAvailableMemberId(cursor):
    cursor.execute("SELECT memberId FROM Member ORDER BY memberId ASC")
    existing_ids = [row[0] for row in cursor.fetchall()]
    new_id = 1
    for eid in existing_ids:
        if eid != new_id:
            break
        new_id += 1
    return new_id

def newMember(args=[""]*11):  # args[9] = classId, args[10] = attendanceDate
    connection = connectDatabase()
    output = ""

    if len(args) < 11:
        args += [""] * (11 - len(args))

    if connection:
        cursor = connection.cursor()
        try:
            member_id = getLowestAvailableMemberId(cursor)

            cursor.execute("""
                INSERT INTO Member (memberId, name, email, phone, address, age, membershipStartDate, membershipEndDate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (member_id, args[0], args[1], args[2], args[3], int(args[4]), args[5], args[6]))

            if args[7] and args[8]:
                cursor.execute("SELECT cost FROM MembershipPlan WHERE planId = ?;", (int(args[7]),))
                cost = cursor.fetchone()
                if cost:
                    amount_paid = cost[0]
                    cursor.execute("""
                        INSERT INTO Payment (memberId, planId, amountPaid, paymentDate)
                        VALUES (?, ?, ?, ?);
                    """, (member_id, int(args[7]), amount_paid, args[8]))

            if args[9] and args[10]:
                cursor.execute("""
                    INSERT INTO Attends (memberId, classId, attendanceDate)
                    VALUES (?, ?, ?);
                """, (member_id, int(args[9]), args[10]))
            else:
                raise ValueError("New member must be assigned at least one class.")

        except Exception as e:
            output += f"Error inserting new member - {e}\n"
        finally:
            connection.commit()
            connection.close()

    print(output)

def updateMember(memId=0, args=[""]*9):
    args += [""] * (9 - len(args))  # Ensure args has at least 9 elements

    connection = connectDatabase()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT name, email, phone, address, age, membershipStartDate, membershipEndDate
                FROM Member WHERE memberId = ?;
            """, (memId,))
            result = cursor.fetchone()
            if not result:
                raise ValueError("Member ID does not exist.")

            for i in range(7):
                if args[i] == "":
                    args[i] = result[i]

            cursor.execute("""
                UPDATE Member
                SET name = ?, email = ?, phone = ?, address = ?, age = ?, membershipStartDate = ?, membershipEndDate = ?
                WHERE memberId = ?;
            """, (*args[:7], memId))

            planId = args[7].strip()
            paymentDate = args[8].strip()

            if planId:
                cursor.execute("SELECT planId FROM MembershipPlan WHERE planId = ?;", (planId,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO MembershipPlan (planId, planType, durationMonths, price)
                        VALUES (?, ?, ?, ?);
                    """, (planId, "Custom", 1, 0.00))

            if planId and paymentDate:
                cursor.execute("""
                    INSERT INTO Payment (memberId, planId, paymentDate)
                    VALUES (?, ?, ?);
                """, (memId, planId, paymentDate))

            connection.commit()
        except Exception as e:
            print(f"Error in updateMember: {e}")
        finally:
            connection.close()

def delMember(memId=0):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                DELETE FROM Payment WHERE memberId = ?;
            """, (memId,))

            cursor.execute("""
                DELETE FROM Member WHERE memberId = ?;
            """, (memId,))
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
            cursor.execute("SELECT * FROM MembershipPlan;")
            members = cursor.fetchall()
            output += "Plan ID | Plan Type | Cost\n" + "-" * 50 + "\n"
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

def getAllMembers(return_output=False):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT M.memberId, M.name, M.email, M.age, MP.planType
                FROM Member M
                LEFT JOIN (
                    SELECT P1.memberId, P1.planId
                    FROM Payment P1
                    WHERE P1.paymentId = (
                        SELECT MAX(P2.paymentId)
                        FROM Payment P2
                        WHERE P2.memberId = P1.memberId
                    )
                ) LatestP ON M.memberId = LatestP.memberId
                LEFT JOIN MembershipPlan MP ON LatestP.planId = MP.planId;
            """)
            members = cursor.fetchall()
            output += "ID | Name | Email | Age | Membership Plan\n" + "-" * 60 + "\n"
            if members:
                for member in members:
                    output += f"{member[0]} | {member[1]} | {member[2]} | {member[3]} | {member[4] if member[4] else 'None'}\n"
            else:
                output += "No members found.\n"
        except sqlite3.Error as error:
            output += f"Error fetching members - {error}\n"
        finally:
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
            cursor.execute("""
                INSERT INTO Attends (memberId, classId, attendanceDate)
                VALUES (?, ?, ?);
            """, (int(args[0]), int(args[1]), args[2]))
        except sqlite3.Error as error:
            output += f"Error adding new attendance - {error}\n"
        finally:
            connection.commit()
            connection.close()
    print(output)

def updateClassAttendee(memberId=0, classId=0, newDate=""):
    connection = connectDatabase()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                UPDATE Attends
                SET classId = ?, attendanceDate = ?
                WHERE memberId = ?;
            """, (classId, newDate, memberId))
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

def assignMemberToClass(memberId, classId):
    connection = connectDatabase()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO ClassAttendance (memberId, classId, attendanceDate) VALUES (?, ?, DATE('now'))", (memberId, classId))
        connection.commit()
        connection.close()

def removeMemberFromClass(memberId, classId):
    connection = connectDatabase()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM ClassAttendance WHERE memberId = ? AND classId = ?", (memberId, classId))
        connection.commit()
        connection.close()

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

