from tkinter import *
from PIL import Image, ImageTk

def open_beginner_plan():
    top = Toplevel()
    top.title("Beginner Plan - Day 1")
    top.geometry("700x500")
    top.config(bg="#121212")

    # --- Title Section ---
    title = Label(
        top,
        text="Day 1: Full Body Beginner Workout",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#121212"
    )
    title.pack(pady=15)

    # --- Exercise Preview Frame ---
    exercise_frame = Frame(top, bg="#1E1E1E", bd=2, relief="ridge")
    exercise_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Sample exercise GIF or image placeholder
    try:
        img = PhotoImage(file="pushup.gif")  # replace with your exercise GIF or static image
    except Exception:
        img = PhotoImage(width=400, height=250)  # fallback empty image

    img_label = Label(exercise_frame, image=img, bg="#1E1E1E")
    img_label.image = img  # keep reference
    img_label.pack(pady=15)

    # Exercise name + duration
    ex_name = Label(
        exercise_frame,
        text="Exercise 1: Push-ups",
        font=("Arial", 14, "bold"),
        fg="white",
        bg="#1E1E1E"
    )
    ex_name.pack()

    duration = Label(
        exercise_frame,
        text="Duration: 30 seconds",
        font=("Arial", 11),
        fg="#bfbfbf",
        bg="#1E1E1E"
    )
    duration.pack(pady=5)

    # --- Bottom Buttons ---
    bottom_frame = Frame(top, bg="#121212")
    bottom_frame.pack(pady=20)

    done_btn = Button(
        bottom_frame,
        text="Done ✅",
        font=("Arial", 12, "bold"),
        bg="#0078D7",
        fg="white",
        width=10,
        relief="flat",
        cursor="hand2",
    )
    done_btn.grid(row=0, column=0, padx=15)

    next_btn = Button(
        bottom_frame,
        text="Next ▶",
        font=("Arial", 12, "bold"),
        bg="#28A745",
        fg="white",
        width=10,
        relief="flat",
        cursor="hand2",
    )
    next_btn.grid(row=0, column=1, padx=15)

    # --- Progress Info ---
    progress = Label(
        top,
        text="Exercise 1 of 10",
        font=("Arial", 11),
        fg="#aaaaaa",
        bg="#121212"
    )
    progress.pack(side="bottom", pady=10)


# 🔹 Run the UI directly for testing
root = Tk()
root.withdraw()  # hide the main Tk window
open_beginner_plan()
root.mainloop()
