from tkinter import *
from tkinter import messagebox,ttk
import mysql.connector as mysql
from PIL import Image,ImageTk

import sys
import subprocess

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

import traceback

con=mysql.connect(host="localhost",user="root",password="Admin@123",database="fitness_db")
cur=con.cursor()
con.commit()

name_entry = type_entry = duration_entry = calories_entry = None
listbox=None
dashboard=None



def register_user():
    name=r1.get()
    email=r2.get()
    username=r3.get()
    password=r4.get()

    if name=="" or email=="" or username=="" or password=="":
        messagebox.showerror("Error","All fields are required")
        return

    cur.execute("SELECT * FROM users_info WHERE username=%s",(username,))

    if cur.fetchone():
        messagebox.showerror("Error","Username already exists")
        return
    
    sql="INSERT INTO users_info(fullname,email,username,password) VALUES (%s,%s,%s,%s)" 
    cur.execute(sql,(name, email, username, password))

    con.commit()
    messagebox.showinfo("Success","Registration successfully")
    r1.delete(0,END);
    r2.delete(0,END);
    r3.delete(0,END);
    r4.delete(0,END);



def login_user():
    username=e1.get()
    password=e2.get()

    if username=="" or password=="":
        print("Error","All fields are required")
        return

    cur.execute("SELECT * FROM users_info where username=%s and password=%s",(username,password))
    result=cur.fetchone()

    if result:
        messagebox.showinfo("Success",f"Welcome {username}")
        open_dashboard(username)
    else:
        messagebox.showerror("Error","Invalid Certificates")

    try:
        e1.delete(0,END);
        e2.delete(0,END);
    except:
        pass
    
def edit(username):
    dashboard_frame.place_forget()  # hide dashboard

    global edit_frame
    edit_frame = Frame(root, bg="#1c1c1c")
    edit_frame.place(relwidth=1, relheight=1)

    create_edit_profile(username)

def create_edit_profile(username):
    # ====== LEFT SIDEBAR ======
    left_frame = Frame(edit_frame, bg="#323334", width=220)
    left_frame.pack(side=LEFT, fill=Y)
    left_frame.pack_propagate(False)

    Label(left_frame, text=username, font=("Arial", 18, "bold"),
          bg="#0204d0", fg="white").pack(pady=20)

    Button(left_frame, text="🏠 Home",
           font=("Times New Roman", 16, "bold"),
           bg="Black", fg="Aqua", width=18,
           command=lambda: back_to_dashboard()).pack(pady=10)

    Button(left_frame, text="📈 Analytics",
           font=("Times New Roman", 16, "bold"),
           bg="Black", fg="Aqua", width=18,
           command=lambda: analytics(username)).pack(pady=10)

    # ====== MAIN EDIT FORM ======
    main_frame = Frame(edit_frame, bg="#1c1c1c")
    main_frame.pack(side=LEFT, fill=BOTH, expand=True)

    Label(main_frame, text="Edit Profile",
          font=("Times New Roman", 22, "bold"),
          bg="#1c1c1c", fg="aqua").pack(pady=20)

    form_frame = Frame(main_frame, bg="#323334", padx=30, pady=30)
    form_frame.pack(pady=40)

    # ---- Form Fields ----
    Label(form_frame, text="Full Name:", bg="#323334", fg="white",
          font=("Times New Roman", 16)).grid(row=0, column=0, sticky="w", pady=10)
    fullname_entry = Entry(form_frame, width=30, font=("Times New Roman", 14))
    fullname_entry.grid(row=0, column=1, pady=10, padx=10)

    Label(form_frame, text="Email:", bg="#323334", fg="white",
          font=("Times New Roman", 16)).grid(row=1, column=0, sticky="w", pady=10)
    email_entry = Entry(form_frame, width=30, font=("Times New Roman", 14))
    email_entry.grid(row=1, column=1, pady=10, padx=10)

    Label(form_frame, text="Username:", bg="#323334", fg="white",
          font=("Times New Roman", 16)).grid(row=2, column=0, sticky="w", pady=10)
    username_entry = Entry(form_frame, width=30, font=("Times New Roman", 14))
    username_entry.grid(row=2, column=1, pady=10, padx=10)

    Label(form_frame, text="Password:", bg="#323334", fg="white",
          font=("Times New Roman", 16)).grid(row=3, column=0, sticky="w", pady=10)
    password_entry = Entry(form_frame, width=30, font=("Times New Roman", 14), show="*")
    password_entry.grid(row=3, column=1, pady=10, padx=10)

    def save_changes():
        new_fullname = fullname_entry.get()
        new_email = email_entry.get()
        new_password = password_entry.get()

        if new_fullname == "" or new_email == "" or new_password == "":
            messagebox.showerror("Error", "All fields are required")
            return

        cur.execute(
            "UPDATE users_info SET fullname=%s, email=%s, password=%s WHERE username=%s",
            (new_fullname, new_email, new_password, username)
        )
        con.commit()
        messagebox.showinfo("Success", "Profile updated successfully!")

    Button(form_frame, text="💾 Save Changes",
           bg="black", fg="aqua",
           font=("Times New Roman", 14, "bold"),
           width=18, command=save_changes).grid(row=4, column=1, pady=30)

    # ---- Auto load DB Values ----
    cur.execute("SELECT fullname,email,username,password FROM users_info WHERE username=%s",
                (username,))
    data = cur.fetchone()

    if data:
        fullname, email, uname, password = data
        fullname_entry.insert(0, fullname)
        email_entry.insert(0, email)
        username_entry.insert(0, uname)
        password_entry.insert(0, password)

def back_to_dashboard():
    edit_frame.destroy()
    dashboard_frame.place(relwidth=1, relheight=1)


def beg(username):
    subprocess.Popen([sys.executable, "test2.py", username])
    root.destroy()

def inter(username):
    root.destroy()
    subprocess.Popen([sys.executable, "inter.py", username])

def adv(username):
    root.destroy()
    subprocess.Popen([sys.executable, "adv.py", username])
    

def open_dashboard(username):    
    global listbox, dashboard_frame
    try:
        header_label.pack_forget()
        login_frame.place_forget()
        register_frame.place_forget()
    except:
        pass

    dashboard_frame = Frame(root, bg="#1c1c1c")
    dashboard_frame.place(relwidth=1, relheight=1)

    # ===== Sidebar (Left Frame) =====
    left_frame = Frame(dashboard_frame, bg="#323334", width=220)
    left_frame.pack(side=LEFT, fill=Y)
    left_frame.pack_propagate(False)

    Label(left_frame, text=username, font=("Arial", 18, "bold"), bg="#0204d0", fg="white").pack(pady=20)

    btn_width = 19

    Button(left_frame, text="🏠 Home", font=("Times New Roman", 16, "bold"),
           bg="Black", fg="Aqua", width=btn_width).pack(pady=5)

    Button(left_frame, text="➕ Add Exercise", font=("Times New Roman", 16, "bold"),
           bg="Black", fg="Aqua", width=btn_width, command=lambda: add_exercise(username)).pack(pady=5)
    
    Button(left_frame, text="✏️ Edit Profile", font=("Times New Roman", 16, "bold"),
           bg="Black", fg="Aqua", width=btn_width, command=lambda:edit(username)).pack(pady=5)
    
    Button(left_frame, text="📈 Analytics", font=("Times New Roman", 16, "bold"),
           bg="Black", fg="Aqua", width=btn_width, command=lambda: analytics(username)).pack(pady=10)

    Button(left_frame, text="Logout", font=("Times New Roman", 16, "bold"),
           bg="black", fg="aqua", width=btn_width, command=lambda: logout(dashboard_frame)).pack(pady=5)


    # ===== Main Content Frame =====
    main_frame = Frame(dashboard_frame, bg="#1c1c1c", padx=20, pady=20)
    main_frame.pack(side=LEFT, fill=BOTH, expand=True)

    # Top welcome frame
    top_frame = Frame(main_frame, bg="#1c1c1c")
    top_frame.pack(side=TOP, fill=X)

    Label(top_frame, text=f"Welcome {username}!", font=("Times New Roman", 20, "bold"),
          bg="#1c1c1c", fg="white").pack(pady=(0,10))

    # ===================== MIDDLE SECTION (Graph + Table) ==========================
    middle_frame = Frame(main_frame, bg="#1c1c1c")
    middle_frame.pack(side=TOP, fill=X, expand=False, pady=10)
    middle_frame.configure(height=300)
    middle_frame.pack_propagate(False)


    # LEFT → Graph
    graph_frame = Frame(middle_frame, bg="#1c1c1c", bd=2, relief=RIDGE, height=200,width=400)
    graph_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,10))
    graph_frame.pack_propagate(False)

    # RIGHT → Table
    bottom_frame = Frame(middle_frame, bg="#1c1c1c")
    bottom_frame.pack(side=LEFT, fill=BOTH, expand=False, padx=(10, 0))

    # ========== Treeview Styling ==========
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Custom.Treeview",
                    background="#262626",
                    foreground="white",
                    fieldbackground="#262626",
                    rowheight=28,
                    font=("Times New Roman", 14))

    style.configure("Custom.Treeview.Heading",
                    background="#333333",
                    foreground="aqua",
                    font=("Segoe UI", 12, "bold"))

    style.map(
    "Custom.Treeview.Heading",
    background=[("active", "#000000"), ("pressed", "#000000")],
    foreground=[("active", "#7CFC00"), ("pressed", "#7CFC00")])

    style.map("Custom.Treeview", background=[("selected", "#0078D7")])

    cols = ("Exercise", "Type", "Duration(min)", "Calories")
    listbox = ttk.Treeview(bottom_frame, columns=cols,
                           show="headings", style="Custom.Treeview")

    for col in cols:
        listbox.heading(col, text=col)
        listbox.column("Exercise", width=180,anchor=CENTER)
        listbox.column("Type", width=130,anchor=CENTER)
        listbox.column("Duration(min)", width=150,anchor=CENTER)
        listbox.column("Calories", width=120,anchor=CENTER)


    listbox.pack(pady=10, fill=BOTH, expand=False)


    # IMPORTANT FIX: Load AFTER listbox is created
    load_exercises(username, graph_frame)

    # ===================== CARDS SECTION ==========================
    bottom_space = Frame(main_frame, bg="#1c1c1c")
    bottom_space.pack(side=TOP, fill=X, pady=(5,5), anchor="center")
    bottom_space.configure(height=420)
    bottom_space.pack_propagate(False)

    

    cards_container = Frame(bottom_space, bg="#1c1c1c")
    cards_container.pack(anchor="center")


    # FIRST CARD
    card_frame = Frame(cards_container, bd=2, relief="groove",bg="#303232", padx=15, pady=15,height=330, width=300)

    card_frame.pack(side=LEFT, padx=20)

    tl = Label(card_frame, text="Beginner 30-Day Plan",
               font=("Times New Roman", 18, "bold"), fg="Aqua", bg="#303232")
    tl.pack(pady=5)

    dl = Label(card_frame,
               text="💪 Perfect for starters!\nBuild consistency and form.\nDuration: 30 Days",
               font=("Times New Roman", 14, "bold"), fg="white", bg="#303232")
    dl.pack(pady=5)

    try:
        img = Image.open("beg.png")
        img = img.resize((220,150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        img_label = Label(card_frame, image=photo, bg="#303232")
        img_label.img = photo
        img_label.pack(pady=5)
    except:
        pass

    Button(card_frame, text="Get Started", bg="Black", fg="Aqua",
           font=("Times New Roman", 16, "bold"), command=lambda: beg(username)).pack(pady=10)

    # SECOND CARD
    card_frame2 = Frame(cards_container, bd=2, relief="groove", bg="#303232", padx=10, pady=10,height=330, width=300)
    card_frame2.pack(side=LEFT, padx=20)

    tl2 = Label(card_frame2, text="Intermediate 30-Day Plan",
                font=("Times New Roman", 18, "bold"), fg="Aqua", bg="#303232")
    tl2.pack(pady=5)

    dl2 = Label(card_frame2,
                text="💥 Push past your limits!\nStrength & endurance.\nDuration: 30 Days",
                font=("Times New Roman", 14, "bold"), fg="white", bg="#303232")
    dl2.pack(pady=5)

    try:
        img2 = Image.open("inter2.png")
        img2 = img2.resize((220,150), Image.LANCZOS)
        p2 = ImageTk.PhotoImage(img2)
        Label(card_frame2, image=p2, bg="#303232").pack(pady=5)
        card_frame2.img = p2
    except:
        pass

    Button(card_frame2, text="Get Started", bg="Black", fg="Aqua",
           font=("Times New Roman", 16, "bold"), command=lambda: inter(username)).pack(pady=10)

    # THIRD CARD
    card_frame3 = Frame(cards_container, bd=2, relief="groove", bg="#303232", padx=30, pady=10,height=330, width=300)
    card_frame3.pack(side=LEFT, padx=20)

    tl3 = Label(card_frame3, text="Advanced 30-Day Plan",
                font=("Times New Roman", 18, "bold"), fg="Aqua", bg="#303232")
    tl3.pack(pady=5)

    dl3 = Label(card_frame3,
                text="🚀 Peak performance!\nIntense challenge.\nDuration: 30 Days",
                font=("Times New Roman", 14, "bold"), fg="white", bg="#303232")
    dl3.pack(pady=5)

    try:
        img3 = Image.open("adv.png")
        img3 = img3.resize((220, 150), Image.LANCZOS)
        p3 = ImageTk.PhotoImage(img3)
        Label(card_frame3, image=p3, bg="#303232").pack(pady=5)
        card_frame3.img = p3
    except:
        pass

    Button(card_frame3, text="Get Started", bg="Black", fg="Aqua",
           font=("Times New Roman", 16, "bold"), command=lambda: adv(username)).pack(pady=10)
    #================================================================================#
    


def add_exercise(username):
    popup = Toplevel(root)
    popup.title("Add Exercise")
    popup.geometry("400x350")

    global name_entry, type_entry, duration_entry, calories_entry  # make them accessible

    Label(popup, text="Exercise Name:").pack(pady=5)
    name_entry = Entry(popup, width=30)
    name_entry.pack()
    
    Label(popup, text="Type:").pack(pady=5)
    type_entry = ttk.Combobox(popup,values=["Strength", "Cardio", "Core", "Flexibility", "Other"])
    type_entry.pack()

    Label(popup, text="Duration (mins):").pack(pady=5)
    duration_entry = Entry(popup, width=30)
    duration_entry.pack()

    Label(popup, text="Calories Burned:").pack(pady=5)
    calories_entry = Entry(popup, width=30)
    calories_entry.pack()
    calories_entry.configure(state='readonly')

    Button(popup, text="Calculate Calories", command=calculate_calories, bg="orange", fg="white").pack(pady=10)
    Button(popup, text="Save", command=lambda:save_exercise(username,popup), bg="green", fg="white").pack(pady=20)

def calculate_calories():
    t=type_entry.get()
    try:
        d=float(duration_entry.get())
    except:
        messagebox.showerror("Error","Duration must be number")
        return

    calorie_chart={"Strength":7,"Cardio":12,"Core":10,"Flexibility":5,"Other":6}
    calories_per_min = calorie_chart.get(t, 6)
    c = calories_per_min * d

    calories_entry.configure(state='normal')
    calories_entry.delete(0, END)
    calories_entry.insert(0, str(c))
    calories_entry.configure(state='readonly')

def save_exercise(username,popup):
    n=name_entry.get()
    t=type_entry.get()

    try:
        d=float(duration_entry.get())
    except:
        messagebox.error("Error","Input must be number")
        return

    calorie_chart={"Strength":7,"Cardio":12,"Core":10,"Flexibility":5,"Other":6}

    calories_per_min = calorie_chart.get(t, 6)
    c = calories_per_min * d

    calories_entry.configure(state='normal')
    calories_entry.delete(0,END)
    calories_entry.insert(0,str(c))
    calories_entry.configure(state='readonly')

    sql="INSERT INTO exercises(name,type,duration,calories,username)VALUES(%s,%s,%s,%s,%s)"
    val=(n,t,d,c,username)

    try:
        cur.execute(sql,val)
        con.commit()
        messagebox.showinfo("Success",f"Exercise'{n}' added! Burned calories{c}")

        if listbox:
            listbox.insert("","end",values=(n,t,d,c))
    
        name_entry.delete(0,END)
        type_entry.set("")
        duration_entry.delete(0,END)
        calories_entry.configure(state='normal')
        calories_entry.delete(0,END)
        calories_entry.delete(0,END)
        calories_entry.configure(state='readonly')

        popup.destroy()

    except:
        messagebox.error("Database Error",str(e))


def load_exercises(username, graph_frame):
    global listbox
    if listbox:
        for item in listbox.get_children():
            listbox.delete(item)

        sql = "SELECT name,type,duration,calories from exercises where username=%s"
        cur.execute(sql, (username,))
        rows = cur.fetchall()

        for row in rows:
            listbox.insert("", "end", values=row)

    # Clear previous graph widgets
    for widget in graph_frame.winfo_children():
        widget.destroy()

    qury = "SELECT date,calories FROM exercises WHERE username=%s ORDER BY date"
    cur.execute(qury, (username,))
    rows = cur.fetchall()

    if rows:
        df = pd.DataFrame(rows, columns=['date','calories'])
        df['date'] = pd.to_datetime(df['date'])

    # --- Compact figure size ---
        fig, ax = plt.subplots(figsize=(6.2, 2.8), dpi=100)
        fig.patch.set_facecolor('#1c1c1c')
        ax.set_facecolor('#1c1c1c')

    # --- Plot (compact marker + line) ---
        sns.lineplot(
            x='date', y='calories', data=df,
            marker='o', markersize=4, linewidth=1.4,
            ax=ax, color='cyan'
            )

    # --- Compact fonts ---
        ax.set_title('Calories Burned Over Time', fontsize=12, color='white')
        ax.set_xlabel('Date', fontsize=10, color='white')
        ax.set_ylabel('Calories', fontsize=10, color='white')
        ax.tick_params(colors='white', labelsize=9)

    # --- Compact grid ---
        ax.grid(True, alpha=0.5, linestyle='--', color='grey')

    # --- Better date formatting ---
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
        ax.tick_params(axis="x", rotation=35)

    # --- Reduce bottom padding so dates fit ---
        fig.subplots_adjust(bottom=0.25, top=0.88)

    # --- Tight layout for perfect fitting ---
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    else:
        Label(graph_frame, text="No exercise to show yet",bg="#1c1c1c", fg="red", font=("Arial",12)).pack(pady=20)
        
    
    
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


def logout(dashboard_frame):
    dashboard_frame.place_forget()
    
    global login_frame, register_frame

    header_label.pack(pady=20)
    login_frame.place(x=300, y=150, width=400, height=400)
    register_frame.place(x=800, y=150, width=400, height=400)


#Sharp_shooter
#==============Interface========#

root=Tk()
root.state("zoomed")
root.title("FITNESS TRACKER")
root.configure(bg="grey")

header_label = Label(root, text=' Welcome to Fitness Tracker', bd=10, fg="Red",
                     font=("Times New", 50, "bold"))
header_label.pack(pady=20)


# === Frames ===


login_frame = Frame(root, bg="lightgrey", bd=6, relief=RIDGE)
#login_frame.place(x=300, y=150, width=400, height=400)

register_frame = Frame(root, bg="lightgrey", bd=5, relief=RIDGE)
#register_frame.place(x=800, y=150, width=400, height=400)


#===Loginwali Frame====
Label(login_frame, text="Login", fg="red", bg="lightgrey",
      font=("Times New Roman", 20, "bold")).pack(pady=10)

Label(login_frame, bd=5,text="Username", fg="black", bg="lightgrey",
      font=("Times New Roman", 13, "bold")).place(x=30, y=80)

Label(login_frame, text="Password", fg="black", bg="lightgrey",
      font=("Times New Roman", 13, "bold")).place(x=30, y=140)


e1 = Entry(login_frame, bd=5, font=("Times New Roman", 12))
e1.place(x=150, y=80, width=200, height=30)

e2 = Entry(login_frame, bd=5, font=("Times New Roman", 12), show="*")
e2.place(x=150, y=140, width=200, height=30)

Button(login_frame, text="Login", bg="blue", fg="white",
       font=("Times New Roman", 12, "bold"), height=1, width=12,command=login_user).place(x=140, y=200)


    

         
#=====Registration Frame========
Label(register_frame, text="Register", fg="red", bg="lightgrey",
      font=("Times New Roman", 20, "bold")).pack(pady=10)

Label(register_frame, text="Full Name", fg="black", bg="lightgrey",
      font=("Times New Roman", 12, "bold")).place(x=30, y=70)

Label(register_frame, text="Email", fg="black", bg="lightgrey",
      font=("Times New Roman", 12, "bold")).place(x=30, y=120)

Label(register_frame, text="Username", fg="black", bg="lightgrey",
      font=("Times New Roman", 12, "bold")).place(x=30, y=170)

Label(register_frame, text="Password", fg="black", bg="lightgrey",
      font=("Times New Roman", 12, "bold")).place(x=30, y=220)


r1 = Entry(register_frame, bd=5, font=("Times New Roman", 12))
r1.place(x=150, y=70, width=200, height=30)

r2 = Entry(register_frame, bd=5, font=("Times New Roman", 12))
r2.place(x=150, y=120, width=200, height=30)

r3 = Entry(register_frame, bd=5, font=("Times New Roman", 12))
r3.place(x=150, y=170, width=200, height=30)

r4 = Entry(register_frame, bd=5, font=("Times New Roman", 12), show="*")
r4.place(x=150, y=220, width=200, height=30)

Button(register_frame, text="Register", bg="green", fg="white",
       font=("Times New Roman", 12, "bold"), height=1, width=12,command=register_user).place(x=140, y=280)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Returned from Edit Profile (or another module)
        logged_in_user = sys.argv[1]
        open_dashboard(logged_in_user)
    else:
        # Normal program start → Show Login/Register
        login_frame.place(x=300, y=150, width=400, height=400)
        register_frame.place(x=800, y=150, width=400, height=400)

    root.mainloop()

