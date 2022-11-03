import getpass
import dbFunctions
import MiniProjectOne

# Functionality for starting the login process
# returns the id of the user/artist and type of user (artist or user)


def getLoginInfo():
    while True:
        id = MiniProjectOne.getInput('ID: ', 'Must input an ID')
        # getPassword() returns err currently
        password = MiniProjectOne.getInput(
            "Password: ", "Must Input a password")

        if (dbFunctions.idInBoth(id)):
            userOrArtist = ""
            while True:
                userOrArtist = input(
                    "ID was found in both tables are you logging in as a User or Artist U/A: ")
                if (userOrArtist == "u"):
                    if (dbFunctions.loginUser(id, password)):
                        return "user", id
                    else:
                        print("Login Failed")
                        break
                elif (userOrArtist == "a"):
                    if (dbFunctions.loginArtist(id, password)):
                        return "artist", id
                    else:
                        print("Login Failed")
                        break
        else:
            result = dbFunctions.attemptLoginBothTables(id, password)
            if (result != None):
                return result, id

            if (result == None):
                register = None
                while True:
                    register = input(
                        "Would you like to register as a new user? Y/N: ")
                    if (register.lower() == "y"):
                        uid = registerUser()
                        return "user", uid
                    elif (register.lower() == "n"):
                        break


def registerUser():
    print("New User Registration")
    id = MiniProjectOne.getInput('ID: ', 'Must input an ID')
    while dbFunctions.checkUserId(id):
        print('That user id is already taken. Please enter a new one')
        id = MiniProjectOne.getInput('ID: ', 'Must input an ID')

    name = MiniProjectOne.getInput('Name: ', 'Must input a name')
    password = MiniProjectOne.getInput('Password: ', 'Must input a password')

    dbFunctions.registerUser(id, name, password)

    return id
