from tkinter import *
from PIL import Image, ImageTk

# --- Workout Data (exercise_name, gif_path, duration_in_seconds) ---
workout = [
    ("Jumping Jacks", "gifs/jumping_jacks.gif", 10),
    ("Squats", "gifs/squats.gif", 10),
    ("Push Ups", "gifs/pushups.gif", 10),
    ("Plank", "gifs/plank.gif", 10),
]

# --- Globals ---
current = 0
remaining = 0
frames = []
vars_list = []

# --- Functions ---
def start_session():
    start_btn.pack_forget()
    show_exercise()

def show_exercise():
    global current
    if current < len(workout):
        name, gif_path, duration = workout[current]
        exercise_label.config(text=f"🏋️‍♀️ {name}")
        show_gif(gif_path)
        start_timer(duration)
    else:
        show_summary()

def show_gif(gif_path):
    global frames
    try:
        frames = [ImageTk.PhotoImage(Image.open(gif_path).copy().convert("RGBA"))]
        image_label.config(image=frames[0], text="")
    except:
        image_label.config(text="[GIF Missing]", fg="red", font=("Arial", 14))

def start_timer(duration):
    global remaining
    remaining = duration
    update_timer()

def update_timer():
    global remaining
    if remaining >= 0:
        timer_label.config(text=f"Time Left: {remaining}s")
        remaining -= 1
        root.after(1000, update_timer)
    else:
        show_rest()

def show_rest():
    exercise_label.config(text="⏸ Rest for 5 seconds")
    image_label.config(image="", text="Rest", fg="yellow", font=("Arial", 18))
    timer_label.config(text="")
    root.after(5000, next_exercise)

def next_exercise():
    global current
    current += 1
    image_label.config(text="")
    show_exercise()

def show_summary():
    exercise_label.config(text="✅ Workout Complete!")
    image_label.config(image="", text="")
    timer_label.config(text="")
    check_window()

def check_window():
    top = Toplevel(root)
    top.title("Mark Completed Exercises")
    top.geometry("400x400")
    top.config(bg="#121212")

    Label(top, text="Select completed exercises:",
          font=("Arial", 14), fg="white", bg="#121212").pack(pady=10)

    global vars_list
    vars_list = []
    for name, _, _ in workout:
        var = BooleanVar()
        Checkbutton(top, text=name, variable=var,
                    bg="#121212", fg="white", font=("Arial", 12),
                    selectcolor="#262626").pack(anchor="w", padx=40)
        vars_list.append((name, var))

    Button(top, text="Confirm", bg="#00ffcc", fg="black", font=("Arial", 14),
           command=save_completed).pack(pady=20)

def save_completed():
    from tkinter import messagebox
    completed = [name for name, var in vars_list if var.get()]
    print("Completed:", completed)
    # Later: insert completed into MySQL
    messagebox.showinfo("Workout", "Session Saved Successfully!")

# --- UI Setup ---
root = Tk()
root.title("Beginner 20-Min Full Body Workout")
root.geometry("800x600")
root.config(bg="#121212")

exercise_label = Label(root, text="", font=("Arial", 22, "bold"), fg="white", bg="#121212")
exercise_label.pack(pady=30)

image_label = Label(root, bg="#121212")
image_label.pack(pady=10)

timer_label = Label(root, text="", font=("Arial", 20), fg="#00ffcc", bg="#121212")
timer_label.pack(pady=20)

start_btn = Button(root, text="Start Session", font=("Arial", 16, "bold"),
                   bg="#00ffcc", fg="black", command=start_session)
start_btn.pack(pady=30)

root.mainloop()
