import tkinter as tk
import auth_system

root = tk.Tk()


root.title("Authentication System")
root.geometry("500x400")


username_label = tk.Label(root, text="Username")
username_label.pack()

username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password")
password_label.pack()

password_entry = tk.Entry(root, show="*")
password_entry.pack()


result_label = tk.Label(root, text="")
result_label.pack()

# Functions 

    # USER
def show_user_window(current_role,current_user):

    user_window = tk.Toplevel(root)
    user_window.title(f"{current_user}")
    user_window.geometry("500x400")


    # ADMIN
def show_admin_window(current_role, current_user):


    admin_window = tk.Toplevel(root)
    admin_window.title(f"{current_user}, you are {current_role}")
    admin_window.geometry("500x400")
    root.withdraw()





def login():
    username = username_entry.get()
    password = password_entry.get()

    current_user, current_role, message = auth_system.authenticate_user(
        username,
        password
    )

    result_label.config(text=message)

    if current_role is not None:
        if current_role == "user":
            show_user_window(current_role, current_user)

        else:
             show_admin_window(current_role, current_user)




button = tk.Button(
    root,
    text="login",
    command=login
)

button.pack()

root.mainloop()
