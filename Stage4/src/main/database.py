import os
import sqlite3


def connectDatabase():
    try:
        # Directly reference the database from the /database directory using absolute path
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'XYZGym.sqlite')
        print(f"Attempting to connect to database at: {db_path}")

        if not os.path.isfile(db_path):
            raise FileNotFoundError(f"Database not found at: {db_path}")

        sqliteConnection = sqlite3.connect(db_path)
        print(f'Connected to SQLite at {db_path}')
        return sqliteConnection
    except (sqlite3.Error, FileNotFoundError) as error:
        print('Error occurred - ', error)
        return None

