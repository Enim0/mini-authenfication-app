# SHOW
def show_profile(current_user, users):
        print(current_user)
        print(users[current_user]["age"])
        print(users[current_user]["country"])


# CHANGE PASSWORD
def change_password(current_user, users, new_password):
    users[current_user]["password"] = new_password
    print("you succsesfuly changed your password")


# DELETE MY ACCOUNT
def delete_my_acc(current_user, users, current_role, password, answer):
    if password != users[current_user]["password"]:
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
        users[which_user]["password"] = new_password
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

users = {
    "alex": {
        "password": "1234",
        "age": 17,
        "country": "Spain",
        "role": "admin"
    },
    "bob": {
        "password": "qwerty",
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

        if login in users:
            if users[login]["password"] == password:
                current_user = login
                current_role = users[login]["role"]

                if current_role == "admin":
                    print(f"Welcome, Dear {login}, you are admin!")
                    while True:
                        sub_command = input("show / show all users / change password / change user password / delete user / delete my account / logout: ")

                        # SHOW
                        if sub_command == "show":
                            show_profile(current_user,users)
                            
                        # SHOW ALL USERS
                        elif sub_command == "show all users":
                            show_all_users(users)
                                
                        # CHANGE_PASSWORD
                        elif sub_command == "change password":
                            new_password = input("write new password")
                            change_password(current_user, users, new_password)
                            
                        # CHANGE USER PASSWORD
                        elif  sub_command == "change user password":
                            new_password = input("write new password")
                            which_user = input("Write for wich user you would like to change password: ")
                            message = change_user_password(new_password, users, which_user, current_user)
                            print(message)
                            
                                
                        # DELETE USER
                        elif sub_command == "delete user": 
                            user_login = input("write user login")
                            answer = input("Are you sure 'only yes or no': ")
                            message = delete_user(user_login, users, current_user, answer)
                            print(message)
                            
                            
                        # DELETE MY ACCOUNT
                        elif sub_command == "delete my account":
                            password = input(f"write your password {current_user}: ")
                            answer = input("are you sure you want to delete your account? ")

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
                            answer = input("do you actually want to logout") 
                            current_user, current_role, message =  logout(current_user, current_role, answer)
                            if current_user is None:
                                print(message)
                                break
                            
                            else:
                                print(message)
                        else:
                            print("error")
                            
                else:
                    print(f"Welcome, Dear {login}")

                    while True:
                        sub_command = input("show / change password / delete my account / logout: ")

                        # SHOW
                        if sub_command == "show":
                            show_profile(current_user,users)

                        # CHANGE_PASSWORD
                        elif sub_command == "change password":
                            new_password = input("write new password")
                            change_password(current_user, users, new_password)

                        # DELETE MY ACCOUNT
                        elif sub_command == "delete my account":
                            password = input(f"write your password {current_user}: ")
                            answer = input("are you sure you want to delete your account? ")

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
                            answer = input("do you actually want to logout") 
                            current_user, current_role, message =  logout(current_user, current_role, answer)
                            if current_user is None:
                                print(message)
                                break
                            
                            else:
                                print(message)
                        else:
                            print("error")
            else:
                print("wrong password")
        else:
            print("login not found")

    # REGISTER
    elif command == "register":
        user_name = input("write username: ")

        if user_name in users:
            print("user already exists")
        else:
            password2 = input("write password: ")
            country = input("write country: ")
            while True:
                try:
                    age = int(input("write age: "))

                    if age > 0:
                        break

                    print("age must be greater than 0")

                except ValueError:
                    print("age must be a number")
                                
            users[user_name] = {
                "password": password2,
                "age": age,
                "country": country,
                "role": "user"
            }
            print("you are registered")
            
    # EXIT
    elif command == "exit":
        break
    
    else:
        print("error")
  
                  