import sqlite3
import time
import dbFunctions
import login
import testQuery


path = "miniProject.db"

def main():
    # Initalizes Connection to the DB - use dbFunctions.Cursor for executing queries  
    dbFunctions.connect(path)

    id, userType = login.getLoginInfo()
    
    testQuery.run(dbFunctions.cursor, dbFunctions.connection)



    dbFunctions.connection.commit()
    dbFunctions.connection.close()
    return


if __name__ == "__main__":
    main()