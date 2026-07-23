import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
ph = PasswordHasher()


# SHOW
def show_profile(current_user, users):
        print(current_user)
        print(users[current_user]["age"])
        print(users[current_user]["country"])


# CHANGE PASSWORD
def change_password(current_user, users, new_password):
    users[current_user]["password"] = ph.hash(new_password)
    print("you succsesfuly changed your password")


# DELETE MY ACCOUNT
def delete_my_acc(current_user, users, current_role, password, answer):
    try:
        ph.verify(
            users[current_user]["password"],
            password
        )

    except VerifyMismatchError:
        return current_user, current_role, "password is wrong"

    if answer != "yes":
        return current_user, current_role, "deletion cancelled" 

    del users[current_user]
    return None, None, "account deleted"

       
# LOGOUT
def logout(current_user, current_role, answer):
    if answer != "yes":
        return current_user, current_role, "logout canceled"
    else:
        return None, None, "you logged out"
    
    
 # ONLY FOR ADMIN !!!


        # SHOW ALL USERS
def show_all_users(users):
    for user_login in users:
        print(user_login)
        print(users[user_login]["age"])
        print(users[user_login]["country"])
        print(users[user_login]["role"])
        print("")
        
                           
        # CHANGE USER PASSWORD
def change_user_password(new_password, users, which_user, current_user):
    if which_user in users and which_user != current_user:
        users[which_user]["password"] = ph.hash(new_password)
        return f"you succsesfuly changed password for {which_user}"
       
    elif which_user == current_user:
            return "use 'change password' to change your own password"
    else:
            return "user doesn not exsist"
        
        
        # DELETE USER 
def delete_user(user_login, users, current_user, answer):
    if user_login in users and user_login != current_user:
        if answer == "yes":
            del users[user_login]
            return  "you deleted user"
        else:
            return "deleting user declained"
    elif user_login == current_user:
        return "you can not delete yourself"
    else:
        return "user doesn't exist"
        
current_user = None
current_role = None

connection = sqlite3.connect("users.db")
cursor = connection.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    country TEXT,
    age INTEGER,
    role TEXT
);
""")


users = {
    "alex": {
        "password": ph.hash("1234"),
        "age": 17,
        "country": "Spain",
        "role": "admin"
    },
    "bob": {
        "password": ph.hash("qwerty"),
        "age": 20,
        "country": "UK",
        "role": "user"
    }
}


while True:
    command = input("Choose login, register, exit: ")

    if command == "login":
        login = input("write your login: ")
        password = input("write password: ")

        cursor.execute(
            "SELECT password, role FROM users WHERE username = ?",
            (login,)
        )

        user = cursor.fetchone()

        if user is None:
            print("user does not exist")
            continue
        else:
            stored_hash = user[0]
            role = user[1]

        try:
            ph.verify(stored_hash, password)

            print("logged in")
            current_user = login
            current_role = role

        except VerifyMismatchError:
            print("password wrong")
            continue
            
        if current_role == "admin":
            print(f"Welcome, Dear {login}, you are admin!")

            while True:
                sub_command = input(
                    "show / show all users / change password / "
                    "change user password / delete user / "
                    "delete my account / logout: "
                )

                # SHOW
                if sub_command == "show":
                    show_profile(current_user, users)

                # SHOW ALL USERS
                elif sub_command == "show all users":
                    show_all_users(users)

                # CHANGE PASSWORD
                elif sub_command == "change password":
                    new_password = input("write new password: ")
                    change_password(current_user, users, new_password)

                # CHANGE USER PASSWORD
                elif sub_command == "change user password":
                    new_password = input("write new password: ")
                    which_user = input(
                        "Write for which user you would like to change password: "
                    )

                    message = change_user_password(
                        new_password,
                        users,
                        which_user,
                        current_user
                    )

                    print(message)

                # DELETE USER
                elif sub_command == "delete user":
                    user_login = input("write user login: ")
                    answer = input("Are you sure? yes or no: ")

                    message = delete_user(
                        user_login,
                        users,
                        current_user,
                        answer
                    )

                    print(message)

                # DELETE MY ACCOUNT
                elif sub_command == "delete my account":
                    password = input(
                        f"write your password {current_user}: "
                    )

                    answer = input(
                        "are you sure you want to delete your account? "
                    )

                    current_user, current_role, message = delete_my_acc(
                        current_user,
                        users,
                        current_role,
                        password,
                        answer
                    )

                    print(message)

                    if current_user is None:
                        break

                # LOGOUT
                elif sub_command == "logout":
                    answer = input("do you actually want to logout? ")

                    current_user, current_role, message = logout(
                        current_user,
                        current_role,
                        answer
                    )

                    print(message)

                    if current_user is None:
                        break

                else:
                    print("error")

        else:
            print(f"Welcome, Dear {login}")

            while True:
                sub_command = input(
                    "show / change password / "
                    "delete my account / logout: "
                )

                # SHOW
                if sub_command == "show":
                    show_profile(current_user, users)

                # CHANGE PASSWORD
                elif sub_command == "change password":
                    new_password = input("write new password: ")
                    change_password(current_user, users, new_password)

                # DELETE MY ACCOUNT
                elif sub_command == "delete my account":
                    password = input(
                        f"write your password {current_user}: "
                    )

                    answer = input(
                        "are you sure you want to delete your account? "
                    )

                    current_user, current_role, message = delete_my_acc(
                        current_user,
                        users,
                        current_role,
                        password,
                        answer
                    )

                    print(message)

                    if current_user is None:
                        break

                # LOGOUT
                elif sub_command == "logout":
                    answer = input("do you actually want to logout? ")

                    current_user, current_role, message = logout(
                        current_user,
                        current_role,
                        answer
                    )

                    print(message)

                    if current_user is None:
                        break

                else:
                    print("error")
                
                
    # REGISTER
    elif command == "register":
        user_name = input("write username: ")
        password2 = input("write password: ")
        hashed_password = ph.hash(password2)
        country = input("write country: ")
        
        
        while True:
            try:
                    age = int(input("write age: "))

                    if age > 0:
                        break
                    print("age must be greater than 0")

            except ValueError:
                    print("age must be a number")
                
        try:
            cursor.execute(
                """
                INSERT INTO users(
                    username,
                    password,
                    country,
                    age,
                    role
                )
                VALUES  (?,?,?,?,?)
                """,
                   
                (
                    user_name,
                    hashed_password,
                    country,
                    age,
                    "user"
                )
            ) 
            connection.commit()
            print("you are registered")
            
            
        except sqlite3.IntegrityError:
            print("user already exists")
                
            
    # EXIT
    elif command == "exit":
        break
    
    else:
        print("error")
  
                  