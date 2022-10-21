import sqlite3
import time
import dbFunctions
import login
import artistMenu
import userMenu

path = "miniProject.db"


def main():
    # Initalizes Connection to the DB - use dbFunctions.Cursor for executing queries
    dbFunctions.connect(path)

    # dbFunctions.createTables()
    # dbFunctions.insert_data()

    userType, id = login.getLoginInfo()
    print(userType, id)

    if (userType == "artist"):
        artistMenu.startMenu(id)
    elif (userType == "user"):
        userMenu.startMenu(id)

    dbFunctions.connection.commit()
    dbFunctions.connection.close()
    return


if __name__ == "__main__":
    main()
