import getpass
import dbFunctions
import userMenu
import artistMenu

# Functionality for starting the login process
# Maybe did this kinda dumb could use a while loop instead of recursion
def startLogin():
    userOrArtistString = input("Type U for User A for Artist: ").lower()
    if (userOrArtistString == "u"):
        registerOrLogin()
    elif (userOrArtistString == "a"):
        login("artists")
    else:
        print("Invalid Input - valid input is U/A \n")
        startLogin()

    return

# Functionality for determing between loging in a user and registering a user
# Maybe did this kinda dumb could use a while loop instead of recursion
def registerOrLogin():
    resgisterOrLogin = input("are you a returnig user Y/N: ").lower()
    if (resgisterOrLogin == "y"):
        login("users")
    elif (resgisterOrLogin == "n"):
        registerUser()
    else:
        print("Invalid Input - valid input is Y/N \n")
        registerOrLogin()

# Handles the login for existing users and artists (note that type should match the table name)
def login(type):
    print("Login Page")
    id = getId()
    password = input("Password: ") #TODO: Replace with getPassword()
    name = dbFunctions.attemptLogin(type, id, password)
    if(name != None):
        # Rediect to correct menu based on type
        print("Logged In")
        if (type == "users"):
            userMenu.startMenu(id, name)
        else:
            artistMenu.startMenu(id, name)
    else:
        # Retry login
        print("Invalid login - try again")
        login(type)

    return

# returns the id of the user/artist and type of user (artist or user)
def getLoginInfo():
    userType = ''
    return id, userType

def displayWelcome():
    title = '''
    ************************************
    *                                  *
    *            Welcome!              *
    *                                  *
    ************************************
    '''

    print(title)

def getId():
    id = input('ID: ')
    return id

def getPassword():
    try:
        password = getpass()
    except Exception as error:
        print('Error: ', error)
    else:
        print(password)
        return password

def registerUser():
    print("New User Registration")
    id = getId()
    while dbFunctions.checkUserId(id):
        print('That user id is already taken. Please enter a new one')
        id = getId()
    
    name = input('Name: ')
    password = input('Password: ')

    dbFunctions.registerUser(id, name, password)
    userMenu.startMenu(id, name)
    
    return 

    