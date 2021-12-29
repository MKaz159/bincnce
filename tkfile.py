import ast
import os
from tkinter import *
from tkinter import messagebox
from dotenv import load_dotenv

load_dotenv()
mainscreen = Tk()

mainscreen.title('Login Screen')
mainscreen.geometry('500x400')
mainscreen.config(bg="#447c84")
mainscreen.resizable(False, False)


class Login_Page:
    def __init__(self, root):
        self.root = root
        frame = Frame(root, padx=20, pady=20)
        frame.pack_propagate(False)
        frame.pack(expand=True)
        self.users_dictionary = ast.literal_eval(os.getenv('users'))

        # LABELS
        Label(
            frame,
            text="Admin Login",
            font=("Times", "24", "bold")
        ).grid(row=0, columnspan=3, pady=10)

        Label(
            frame,
            text="Enter Username",
            font=("Times", "11", "bold")
        ).grid(row=1, column=1, columnspan=3, pady=10)

        Label(
            frame,
            text='Enter Password',
            font=("Times", "14")
        ).grid(row=2, column=1, pady=5)  # .place(x=50, y=110)

        # ENTRIES
        username = StringVar()
        password = StringVar()
        self.usernameEntry = Entry(frame, width=20, textvariable=username)
        self.passwordEntry = Entry(frame, width=20, show='*',textvariable=password)
        self.usernameEntry.grid(row=1, column=2)
        self.passwordEntry.grid(row=2, column=2)

        # Button

        login_button = Button(
            frame,
            text="Login",
            padx=20,
            pady=10,
            relief=RAISED,
            font=("Times", "14", "bold"),
            command=self.validateLogin
        )
        login_button.grid(row=3, column=2, pady=10)

    def validateLogin(self):
        check_counter = 0
        user_input = self.usernameEntry.get()
        password_input = self.passwordEntry.get()
        if user_input == '':
            warn = 'Username Cannot be empty'
        else:
            check_counter += 1
        if password_input == '':
            warn = 'Password cannot be empty'
        else:
            check_counter += 1
        if check_counter == 2:
            for i in range(len(self.users_dictionary['username'])):
                if user_input == self.users_dictionary['username'][i] and password_input == \
                        self.users_dictionary['Password'][i]:
                    self.root.destroy()
                    print('It WORKS')

                    # SUPER IMPORTANT
                    return None
                else:
                    messagebox.showerror('', 'invalid username or password')
        else:
            messagebox.showerror('', warn)


Login_Page(mainscreen)
mainscreen.mainloop()
