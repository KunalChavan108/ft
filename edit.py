from tkinter import *
from tkinter import messagebox,ttk
import importlib
import mysql.connector as mysql

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates


import os
import sys
import subprocess

username=sys.argv[1] if len(sys.argv)>1 else "Guest"
conn=mysql.connect(host="localhost",user="root",database="fitness_db",password="Admin@123")
cur=conn.cursor()
    

def save_changes():
    new_fullname=fullname_entry.get()
    new_email=email_entry.get()
    new_password=password_entry.get()

    if new_fullname=="" or new_email=="" or new_password=="":
        messagebox.showerror("Error","All field are required")
        return

    try:
        cur.execute("UPDATE users_info SET fullname=%s, email=%s, password=%s WHERE username=%s",
                    (new_fullname, new_email, new_password, username))
        conn.commit()
        messagebox.showinfo("Success","Profile updated successfully!")

    except Exception as e:
        messagebox.showerror("Error","All fields are required")

    
    

def analytics(username):
    ana = Toplevel(root)
    ana.title("Calories Burned Analytics")
    ana.geometry("700x500")
    qury = "SELECT date, calories FROM exercises where username=%s ORDER BY date"
    cur.execute(qury,(username,))
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=['date', 'calories'])
    if df.empty:
        Label(ana, text="No exercise data to display.", fg="red").pack(pady=20)
        return
    df['date'] = pd.to_datetime(df['date'])
    fig, ax = plt.subplots(figsize=(7,5))
    sns.lineplot(x='date', y='calories', data=df, marker='o', ax=ax)

    ax.set_title('Calories Burned')
    ax.set_xlabel('Date')
    ax.set_ylabel('Calories')
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))

    fig.autofmt_xdate()
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    canvas = FigureCanvasTkAgg(fig, master=ana)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)




def home():
    root.quit()
    root.destroy()
    subprocess.Popen([sys.executable, "ft.py", username])


root=Tk()
root.title("Edit Profile")
root.state("zoomed")
root.lift()
root.focus_force()
root.update()
root.configure(bg="black")

#========================== LEFTFRAME ============================================#
left_frame=Frame(root,bg="#323334",width=220)
left_frame.pack(side=LEFT,fill=Y)
left_frame.propagate(False)

btn_width=16

Label(left_frame, text=username, font=("Arial", 18, "bold"), bg="#0204d0", fg="white").pack(pady=20)

Button(left_frame, text="🏠 Home", font=("Times New Roman", 16, "bold"),bg="Black", fg="Aqua",
       width=btn_width,command=home).pack(pady=10)

Button(left_frame, text="📈 Analytics",font=("Times New Roman", 16, "bold"),
       bg="Black", fg="Aqua",width=btn_width, command=lambda: analytics(username)).pack(pady=10)


#============================ MID FRAME ================================================#
main_frame = Frame(root, bg="#1c1c1c")
main_frame.pack(side=LEFT, fill=BOTH, expand=True)

Label(main_frame, text="Edit Profile", font=("Times New Roman", 22, "bold"),
      bg="#1c1c1c", fg="aqua").pack(pady=20)

form_frame = Frame(main_frame, bg="#323334", padx=30, pady=30)
form_frame.pack(pady=40)

Label(form_frame, text="Full Name:", font=("Times New Roman", 16),
      bg="#323334", fg="white").grid(row=0, column=0, sticky="w", pady=10)

fullname_entry = Entry(form_frame, width=30, font=("Times New Roman", 14))
fullname_entry.grid(row=0, column=1, pady=10, padx=10)

Label(form_frame, text="Email:", font=("Times New Roman", 16),
      bg="#323334", fg="white").grid(row=1, column=0, sticky="w", pady=10)

email_entry = Entry(form_frame, width=30, font=("Times New Roman", 14))
email_entry.grid(row=1, column=1, pady=10, padx=10)

Label(form_frame, text="Username:", font=("Times New Roman", 16),
      bg="#323334", fg="white").grid(row=2, column=0, sticky="w", pady=10)

username_entry = Entry(form_frame, width=30, font=("Times New Roman", 14))
username_entry.grid(row=2, column=1, pady=10, padx=10)


Label(form_frame, text="Password:", font=("Times New Roman", 16),
      bg="#323334", fg="white").grid(row=3, column=0, sticky="w", pady=10)

password_entry = Entry(form_frame, width=30, font=("Times New Roman", 14), show="*")
password_entry.grid(row=3, column=1, pady=10, padx=10)

Button(form_frame, text="💾 Save Changes", bg="black", fg="aqua",
       font=("Times New Roman", 14, "bold"), width=18,
       command=save_changes).grid(row=4, column=1, pady=30)


try:
    cur.execute("SELECT fullname,email,username,password FROM users_info where username=%s",
                (username,))
    data=cur.fetchone()
    print("DB RESULT:",data)
    if data:
        fullname,email,db_username,password=data
        fullname_entry.insert(0,fullname)
        email_entry.insert(0,email)
        username_entry.insert(0,db_username)
        password_entry.insert(0,password)

except Exception as e:
    print("Error details",e)


root.mainloop()
