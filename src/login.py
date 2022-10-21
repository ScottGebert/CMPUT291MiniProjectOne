import getpass

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
    id = getId()
    while checkIfUserExists(id):
        print('That user id is already taken. Please enter a new one')
        id = getId()
    
    name = input('Name: ')
    password = input('Password: ')

def checkIfUserExists(id):
    return False

    