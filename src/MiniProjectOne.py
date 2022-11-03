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
    run = True
    while run:
        userType, id = login.getLoginInfo()

        if (userType == "artist"):
            run = artistMenu.menu(id)
        elif (userType == "user"):
            run = userMenu.menu(id)


    dbFunctions.connection.commit()
    dbFunctions.connection.close()
    return


def getInput(message, errMessage):
    while True:
        toRet = input(message)
        if (toRet == ""):
            print(errMessage)
        else:
            return toRet


if __name__ == "__main__":
    main()
