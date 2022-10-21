import sqlite3
import time
import dbFunctions
import login


path = "miniProject.db"

def main():
    # Initalizes Connection to the DB - use dbFunctions.Cursor for executing queries  
    dbFunctions.connect(path)
    
    # dbFunctions.createTables()
    # dbFunctions.insert_data()


    userType, id = login.getLoginInfo()

    print(userType, id)


    dbFunctions.connection.commit()
    dbFunctions.connection.close()
    return


if __name__ == "__main__":
    main()