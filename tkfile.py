import os
import tkinter
from tkinter import *
from functools import partial
from dotenv import load_dotenv
import ast

load_dotenv()


class Login_Page:
    def __init__(self, root):
        self.root = root
        self.root.title('Login Page')
        self.root.geometry('400x150')
        self.root.config(bg='#021e2f')
        self.users_dictionary = ast.literal_eval(os.getenv('users'))
        Label(self.root, text="User Name").grid(row=0, column=0)
        username = StringVar()
        self.usernameEntry = Entry(self.root, textvariable=username)
        self.usernameEntry.grid(row=0, column=1)
        Label(self.root, text="Password").grid(row=1, column=0)
        password = StringVar()
        self.passwordEntry = Entry(self.root, textvariable=password, show='*')
        self.passwordEntry.grid(row=1, column=1)
        loginButton = Button(self.root, text="Login", command=self.validateLogin).grid(row=4, column=0)

    def validateLogin(self):
        user_input = self.usernameEntry.get()
        password_input = self.passwordEntry.get()
        for i in range(len(self.users_dictionary['username'])):
            if user_input == self.users_dictionary['username'][i] and password_input == self.users_dictionary['Password'][i]:
                print('found the user')
                return True
        print('not found ')
        return False



mainscreen = Tk()
Login_Page(mainscreen)
mainscreen.mainloop()
