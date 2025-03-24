import sys
import sqlite3

#--------------------------------------------------------------------------------------------------------------------

def connectDatabase():
    try:
        sqliteConnection = sqlite3.connect('sql.db')
        cursor = sqliteConnection.cursor()
    
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)
 
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')

#--------------------------------------------------------------------------------------------------------------------

def main():
    return

#--------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()