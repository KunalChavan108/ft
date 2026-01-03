from tkinter import *
import edit   # <--- import the other file

def open_second_window():
    username = username_entry.get()
    if username:
        second_window.open_window(root, username)

root = Tk()
root.geometry("400x300")
root.title("Main Window")

Label(root, text="Enter Username:", font=("Arial", 14)).pack(pady=10)
username_entry = Entry(root, font=("Arial", 14))
username_entry.pack(pady=10)

Button(root, text="Open Second Window",
       font=("Arial", 14),
       command=open_second_window).pack(pady=20)

root.mainloop()
