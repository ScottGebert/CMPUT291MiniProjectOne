import sqlite3
import time
import dbFunctions
import login
import artistMenu
import userMenu

path = "miniProject.db"


def getInput(message, errMessage):
    while True:
        toRet = input(message)
        if (toRet ==""):
            print(errMessage)
        else:
            return toRet

def main():
    # Initalizes Connection to the DB - use dbFunctions.Cursor for executing queries
    dbFunctions.connect(path)

    # dbFunctions.createTables()
    # dbFunctions.insert_data()

    userType, id = login.getLoginInfo()

    if (userType == "artist"):
        artistMenu.startMenu(id)
    elif (userType == "user"):
        userMenu.startMenu(id)

    dbFunctions.connection.commit()
    dbFunctions.connection.close()
    return


if __name__ == "__main__":
    main()
