import os
import sys
import sqlite3

# Add src/ to sys.path dynamically, so main.* imports work regardless of IDE
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, ".."))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from main.database import connectDatabase
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

def run_query():
    print("\nWelcome to the Gym Management System")
    print("Select a query:")
    print(" 1. Get all members")
    print(" 2. Count classes per gym")
    print(" 3. Get members by class (requires class ID)")
    print(" 4. List equipment by type (requires type name)")
    print(" 5. Get expired memberships")
    print(" 6. Get classes by instructor (requires instructor ID)")
    print(" 7. Calculate average age of members")
    print(" 8. Top instructors")
    print(" 9. Find members by class type (requires class type)")
    print("10. Recent class attendance")
    print("checkdatabase. Check database table structure")
    print("exit. Exit the program")

    query_number = input("\nEnter query number or command: ").strip().lower()

    if query_number == "exit":
        print("Exiting program. Goodbye!")
        sys.exit(0)

    try:
        if query_number == "1":
            connection = connectDatabase()
            if connection:
                getAllMembers()
        elif query_number == "2":
            countClassesPerGym()
        elif query_number == "3":
            class_id = input("Enter class ID: ").strip()
            getMembersByClass(int(class_id))
        elif query_number == "4":
            equipment_type = input("Enter equipment type: ").strip()
            listEquipmentByType(equipment_type)
        elif query_number == "5":
            getExpiredMemberships()
        elif query_number == "6":
            instructor_id = input("Enter instructor ID: ").strip()
            getClassesByInstructor(int(instructor_id))
        elif query_number == "7":
            calculateAverageAge()
        elif query_number == "8":
            topInstructors()
        elif query_number == "9":
            class_type = input("Enter class type: ").strip()
            findMembersByClassType(class_type)
        elif query_number == "10":
            recentClassAttendance()
        elif query_number == "checkdatabase":
            checkDatabase()
        else:
            print("Invalid query. Please try again.")
    except Exception as e:
        print(f"An error occurred while processing the query: {e}")

#--------------------------------------------------------------------------------------------------------------------

def main():
    while True:
        run_query()
        while True:
            satisfied = input("\nWould you like to continue? (Y/N): ").strip().upper()
            if satisfied == "Y":
                break  # Go back to the main menu
            elif satisfied == "N":
                print("Exiting program. Goodbye!")
                return  # Exit program
            else:
                print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")

#--------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
