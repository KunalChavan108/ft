from tkinter import *
import importlib
from PIL import Image, ImageTk,ImageSequence
import winsound
import mysql.connector as mysql

import os
import sys
import subprocess

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates



import threading
from tkinter import filedialog,messagebox

username=sys.argv[1] if len(sys.argv)>1 else "Guest"

conn=mysql.connect(host="localhost",user="root",database="fitness_db",password="Admin@123")
cur=conn.cursor()

workout=[
    ("Jumping Jacks", "gifs/jumping_jacks.gif", 5),
    ("Squats", "gifs/squats.gif", 5),
    ("Push Ups", "gifs/pushups.gif", 5),
    ("Plank", "gifs/plank.gif", 5),
    ]

animating = False
animation_job = None

current=0
remaining=0
frames=[]
vars_list=[]

gif_job=None
music_path=None
music_playing=False

auto_music_enabled=True
session_active=True

def select_music():
    global music_path
    file=filedialog.askopenfilename(
        title="Select Workout Music",
        filetypes=[("WAV Files","*.wav")]
        )
    if file:
        music_path=file
        music_label.config(text=f"🎵 {os.path.basename(file)} selected", fg="lightgreen")
    else:
        music_label.config(text="❌ No file selected",fg="red")

def play_music():
    global music_playing,auto_music_enabled
    if music_path and not music_playing:
        music_playing=True
        auto_music_enabled=True
        winsound.PlaySound(music_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
    elif not music_path:
        messagebox.showerror("No music","Please select one")

def stop_music():
    global music_playing,auto_music_enabled
    winsound.PlaySound(None,winsound.SND_PURGE)
    music_playing=False
    auto_music_enabled=False

def start_session():
    univ_card.place_forget()                    # use place_forget instead of pack_forget
    left_frame.pack_forget()                    # ok because left_frame uses pack
    workout_frame.pack(fill=BOTH,expand=True)   # You can now load your workout screen here
    
    show_exercise()
    if auto_music_enabled:
        play_music()


def show_exercise():
    global current
    if current<len(workout):
        name,gif_path,duration=workout[current]
        
        exercise_label.config(text=f"{name}")
        show_gif(gif_path)
        start_timer(duration)   
        
    else:
        show_summary()

def show_gif(gif_path):
    global frames, frame_index, animating, animation_job

    animating = True  # start animation
    if animation_job:
        root.after_cancel(animation_job)
        animation_job = None

    try:
        img = Image.open(gif_path)
        frames = []
        frame_index = 0
        try:
            while True:
                frame = img.copy().resize((600, 600))
                frames.append(ImageTk.PhotoImage(frame))
                img.seek(len(frames))
        except EOFError:
            pass

        def update_gif():
            global frame_index, animation_job
            if not animating:
                return
            if frames:
                frame = frames[frame_index]
                image_label.config(image=frame)
                image_label.image = frame
                frame_index = (frame_index + 1) % len(frames)
                animation_job = root.after(100, update_gif)

        update_gif()

    except Exception as e:
        image_label.config(text=f"[GIF MISSING] {e}", fg="red")

         
def start_timer(duration):
    global remaining
    remaining=duration
    update_timer()

def update_timer():
    global remaining, current,session_active

    if not session_active:
        return

    if remaining >= 0 and session_active and timer_label.winfo_exists():
        timer_label.config(text=f"Time left: {remaining}s")
        remaining -= 1
        root.after(1000, update_timer)

    else:
        # ✅ Check if current exercise is the last one
        if current + 1 < len(workout):
            show_rest()
        else:
            show_summary()


def show_rest():
    global rest_time, animating, animation_job
    animating = False  # stop GIF animation

    # Cancel running gif animation (important fix)
    if animation_job:
        root.after_cancel(animation_job)
        animation_job = None

    rest_time = 5  # rest duration in seconds

    if current + 1 < len(workout):
        next_name, next_gif, _ = workout[current + 1]
        exercise_label.config(text=f"⏸ Rest Time!\nNext: {next_name}", fg="yellow")

        try:
            img = Image.open(next_gif)
            img = img.resize((300, 300))
            frame = ImageTk.PhotoImage(img)
            image_label.config(image=frame, text="")
            image_label.image = frame
        except:
            image_label.config(text="[PREVIEW MISSING]", fg="red", image="")
    else:
        exercise_label.config(text="🏁 Final Rest!", fg="green")
        image_label.config(text="Almost Done!", font=("Times New Roman",16,"bold"), fg="white", image="")

    update_rest_timer()



def update_rest_timer():
    global rest_time,current
    if rest_time > 0:
        timer_label.config(text=f"Next exercise starts in {rest_time}s", fg="#00ffcc")
        rest_time -= 1
        root.after(1000, update_rest_timer)
    else:
        if current+1<len(workout):
            timer_label.config(text="Starting next exercise...",fg="lightgreen")
            root.after(1000,next_exercise)
        else:
            timer_label.config(text="Session complete",fg="#00ffcc")
            root.after(1000,show_summary)

def next_exercise():
    global current
    current += 1
    if current < len(workout):
        show_exercise()  # ✅ Just call show_exercise(), no args
    else:
        exercise_label.config(text="")
        image_label.config(text="")
        show_summary()


def show_summary():
    global session_active, animating, animation_job
    session_active = False
    animating = False

    # Stop any old animation
    if animation_job:
        root.after_cancel(animation_job)

    # Clear old labels
    exercise_label.config(text="✅ Workout Complete!", fg="#00ffcc", font=("Arial", 22, "bold"))
    timer_label.config(text="Great Job!", fg="#00ffcc", font=("Arial", 20))
    image_label.config(image="", text="")

    # Stop background music
    stop_music()

    # ---- Show Completion GIF ----
    try:
        gif_path = r"C:\Users\guddu\OneDrive\Desktop\ft\gifs\complete.gif"
        gif = Image.open(gif_path)
        frames = [ImageTk.PhotoImage(frame.copy().resize((400, 400))) for frame in ImageSequence.Iterator(gif)]

        def animate(i=0):
            frame = frames[i]
            image_label.config(image=frame)
            image_label.image = frame
            root.after(100, animate, (i + 1) % len(frames))

        animate()

    except Exception as e:
        image_label.config(text=f"[GIF Error: {e}]", fg="red")

    # ---- Save session data ----
    try:
        total_duration = sum(w[2] for w in workout)
        total_minutes=total_duration/60
        calories_per_minute=8
        total_calories = total_minutes * calories_per_minute
        cur.execute(
            "INSERT INTO exercises(name, type, duration, calories, username) VALUES (%s, %s, %s, %s, %s)",
            ("Beginner Full Body", "Cardio", total_minutes, total_calories, username)
        )
        conn.commit()
        messagebox.showinfo("Session Saved", f"Workout saved!\nCalories burned: {total_calories:.1f}")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def home():
    stop_music()
    root.destroy()
    pythonw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    subprocess.Popen([pythonw, "ft.py", username])


    
def back():
    global current,animating,animation_job
    animating=False
    if animation_job:
        root.after_cancel(animation_job)
        animation_job=None

    stop_music()
    current=0

    exercise_label.config(text="")
    timer_label.config(text="")
    image_label.config(image="",text="")

    
    workout_frame.pack_forget()
    univ_card.place(x=450,y=20)   
    left_frame.pack(side=LEFT,fill=Y)

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


    

root=Tk()
root.title("Beginner's Plan")
root.state("zoomed")
root.configure(bg="black")


#========================== LEFT FRAME ===================================#
left_frame = Frame(root, bg="#323334", width=220)
left_frame.pack(side=LEFT, fill=Y)
left_frame.pack_propagate(False)

btn_width = 18

Button(left_frame,text="🏠 Home",font=("Times New Roman", 14, "bold"),bg="Black",fg="Aqua",
    width=btn_width,command=home).pack(pady=5)

Button(left_frame, text="✏️ Edit Profile", font=("Times New Roman", 14, "bold"),
    bg="Black", fg="Aqua", width=btn_width).pack(pady=5)
    
Button(left_frame, text="📈 Analytics",font=("Times New Roman", 14, "bold"),
       bg="Black", fg="Aqua",width=btn_width, command=lambda: analytics(username)).pack(pady=10)






#======================== UNIVERSAL CARD ========================================#
univ_card = Frame(root, width=800, height=200, bg="#3e3d41", relief="groove")
univ_card.place(x=450, y=20)
univ_card.propagate(True)

Label(univ_card, text="BEGINNER SESSION", fg="Aqua", bg="#3e3d41",
      font=("Times New Roman", 16, "bold")).pack(pady=10)

try:
    image = Image.open("beg.png").resize((600, 300), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    img_label = Label(univ_card, image=photo, bg="#3e3d41")
    img_label.image = photo
    img_label.pack(pady=5)
except FileNotFoundError:
    print("Image Not Found")

Label(
    univ_card,
    text=("""
  This guided workout is designed for complete beginners to build strength, flexibility,
  and stamina — all in just 20 minutes a day. Perform this session daily for at least 10 days 
  to experience visible improvements in your energy, posture, and confidence.

  Once you complete 10 days consistently, you’ll be ready to unlock the Next Level Session
  for intermediate training!
"""),
    fg="White",
    bg="#3e3d41",
    font=("Times New Roman", 14, "bold"),
    justify=LEFT,
).pack(pady=10)


music_frame=Frame(univ_card,bg="#3e3d41")
music_frame.pack(pady=10)

Label(music_frame,text="🎶 Select Workout Music:",fg="white",bg="#3e3d41",font=("Times New Roman",14,"bold")).pack()
Button(music_frame,text="Browse Music",font=("Times New Roman",12,"bold"),fg="black",bg="#00ffcc",command=select_music).pack(pady=5)

music_label=Label(music_frame,text="No file selected",fg="red",bg="#3e3d41")
music_label.pack()

Button(music_frame,text="Play Music",font=("Arial",12,"bold"),bg="#f44336",fg="white",command=play_music).pack(side=LEFT,padx=10)

Button(music_frame,text="Stop Music",font=("Arial", 12, "bold"),bg="#f44336",fg="white",command=stop_music).pack(side=LEFT, padx=10)




start = Button(
    univ_card,
    text="Start Session",
    font=("Arial", 16, "bold"),
    bg="#00ffcc",
    fg="black",
    command=start_session
)
start.pack(pady=20)



#================================ WORKOUT FRAME ========================================#
workout_frame = Frame(root, bg="#121212")

exercise_label = Label(workout_frame, text="", font=("Arial", 22, "bold"),
                       fg="white", bg="#121212")
exercise_label.pack(pady=20)

gif_container=Frame(workout_frame,bg="#121212")
gif_container.pack(fill=BOTH,expand=True)

image_label = Label(workout_frame, bg="#121212")
image_label.pack(expand=True)

timer_label = Label(workout_frame, text="", font=("Arial", 20),
                    fg="#00ffcc", bg="#121212")
timer_label.pack(pady=10)


exit_btn=Button(workout_frame,text="⬅ Exit Session",font=("Arial", 12, "bold"),
    bg="#00ffcc",fg="black",command=back)
exit_btn.pack(pady=10)

exit_btn.lift()

root.protocol("WM_DELETE_WINDOW",lambda:(conn.close(),root.destroy()))

root.mainloop()



