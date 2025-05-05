import os
import sys
import sqlite3

# Add src/ to sys.path dynamically, so main.* imports work regardless of IDE
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, ".."))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from database import connectDatabase
from functions import countClassesPerGym, listEquipmentByType, getClassesByInstructor, topInstructors, \
    recentClassAttendance
from functions import getAllMembers, getMembersByClass, getExpiredMemberships, calculateAverageAge, \
    findMembersByClassType

#--------------------------------------------------------------------------------------------------------------------

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

    query_number = sys.argv[1].lower()

    try:
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
        elif query_number == "checkdatabase":
            checkDatabase()
        else:
            print("Invalid query or parameters. Please check the usage.")
    except Exception as e:
        print(f"An error occurred while processing the query: {e}")

#--------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

