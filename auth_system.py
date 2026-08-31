import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
ph = PasswordHasher()

 
def authenticate_user(login, password):
    cursor.execute(
        """
        SELECT password, role
        FROM users
        WHERE username = ?
        """,
        (login,)
    )

    user_data = cursor.fetchone()

    if user_data is None:
        return None, None, "user does not exist"

    stored_hash = user_data[0]
    role = user_data[1]
    
    try:
        ph.verify(
            stored_hash,
            password
        )
        return login, role, "logged in"
        
        
    except VerifyMismatchError:
       return None, None, "password is wrong"
            
   

# SHOW
def show_profile(current_user):
    cursor.execute("""
    SELECT username, age, country FROM users WHERE username = ?
    """,
    (current_user,)
    )
    
    user_data = cursor.fetchone()
    username, age, country = user_data
    print(username)
    print(age)
    print(country)
    

# CHANGE PASSWORD
def change_password(current_user, new_password):
    new_hashed_password = ph.hash(new_password)

    cursor.execute(
        """
        UPDATE users
        SET password = ?
        WHERE username = ?
        """,
        (
            new_hashed_password,
            current_user
        )
    )

    connection.commit()


# DELETE MY ACCOUNT
def delete_my_acc(current_user, current_role, password, answer):
        cursor.execute(
            """
            SELECT password FROM users WHERE username = ?
            """,
            (current_user,)
        )

        user_data = cursor.fetchone()
        stored_hash = user_data[0]

        try:
            ph.verify(
                stored_hash,
                password
            )

        except VerifyMismatchError:
            return current_user, current_role, "password is wrong"

        if answer != "yes":
            return current_user, current_role, "deletion cancelled"

        cursor.execute(
            """
            DELETE FROM users
            WHERE username = ?;
            """,
            (current_user,)
        )
        
        connection.commit()
        
        return None, None, "account deleted"

       
# LOGOUT
def logout(current_user, current_role, answer):
    if answer != "yes":
        return current_user, current_role, "logout canceled"
    else:
        return None, None, "you logged out"
    
    
 # ONLY FOR ADMIN !!!


        # SHOW ALL USERS
def show_all_users():
    cursor.execute("""
    SELECT username, age, country, role FROM users
    """)
    
    details = cursor.fetchall()

    for username, age, country, role in details:
        print(username)
        print(age)
        print(country)
        print(role)
        
        
                           
        # CHANGE USER PASSWORD
def change_user_password(new_password,  which_user, current_user):
    if which_user == current_user:
        return"Your password you can change only in change password"
  
    
    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (which_user,)
    )
    
    user = cursor.fetchone()
    
    if user is None:
        return"user does not exsist"
    
    hashed_password = ph.hash(new_password)
    
    cursor.execute(
        """
        UPDATE users
        SET password = ?
        WHERE username = ?
        """,
        (hashed_password, which_user)
    )       
    connection.commit()
       
    return f"you successfully changed password for {which_user}"
    
        
        # DELETE USER 
def delete_user(user_login, current_user, answer):
    if user_login == current_user:
        return "You can not delete your account here"

    cursor.execute(
        """
        SELECT username FROM users
        WHERE username = ?
        """,
        (user_login,)
    )

    user_data = cursor.fetchone()

    if user_data is None:
        return "user does not exist"

    if answer != "yes":
        return "deleting user cancelled"

    cursor.execute(
        """
        DELETE FROM users
        WHERE username = ?
        """,
        (user_login,)
    )

    connection.commit()

    return f"{user_login} successfully deleted"
   
        
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



def main():
  while True:
    command = input("Choose login, register, exit: ")

    if command == "login":
        login = input("write your login: ")
        password = input("write password: ")

        current_user, current_role, message = authenticate_user(login, password)
        print(message)
        
        if current_user is None:
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
                    show_profile(current_user)

                # SHOW ALL USERS
                elif sub_command == "show all users":
                    show_all_users()

                # CHANGE PASSWORD
                elif sub_command == "change password":
                    new_password = input("write new password: ")
                    change_password(current_user, new_password)

                # CHANGE USER PASSWORD
                elif sub_command == "change user password":
                    new_password = input("write new password: ")
                    which_user = input(
                        "Write for which user you would like to change password: "
                    )

                    message = change_user_password(
                        new_password,
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
                    show_profile(current_user)

                # CHANGE PASSWORD
                elif sub_command == "change password":
                    new_password = input("write new password: ")
                    change_password(current_user, new_password)

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
  
if __name__ == "__main__":
    main()