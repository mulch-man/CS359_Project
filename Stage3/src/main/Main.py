import sqlite3
import sys

from database import connectDatabase
from main.functions import countClassesPerGym, listEquipmentByType, getClassesByInstructor, topInstructors, \
    recentClassAttendance
from main.functions import getAllMembers, getMembersByClass, getExpiredMemberships, calculateAverageAge, \
    findMembersByClassType


# Check database tables

def checkDatabase():
    connection = connectDatabase()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print("Tables in the database:")
            for table in tables:
                print(table[0])
        except sqlite3.Error as error:
            print('Error checking database - ', error)
        finally:
            connection.close()

#--------------------------------------------------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python Main.py <query_number> [additional_params]")
        return

    query_number = sys.argv[1]

    if query_number == "1":
        connection = connectDatabase()
        if connection:
            getAllMembers()
    elif query_number == "2":
        countClassesPerGym()
    elif query_number == "3" and len(sys.argv) == 3:
        getMembersByClass(int(sys.argv[2]))
    elif query_number == "4" and len(sys.argv) == 3:
        listEquipmentByType(sys.argv[2])
    elif query_number == "5":
        getExpiredMemberships()
    elif query_number == "6" and len(sys.argv) == 3:
        getClassesByInstructor(int(sys.argv[2]))
    elif query_number == "7":
        calculateAverageAge()
    elif query_number == "8":
        topInstructors()
    elif query_number == "9" and len(sys.argv) == 3:
        findMembersByClassType(sys.argv[2])
    elif query_number == "10":
        recentClassAttendance()
    elif query_number.lower() == "checkdatabase":
        checkDatabase()
    else:
        print("Invalid query or parameters. Please check the instructions.")

#--------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
