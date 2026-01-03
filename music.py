import winsound
from tkinter import *

AUDIO=r"C:\Users\guddu\OneDrive\Desktop\ft\la caution.wav"

def play_music():
    winsound.PlaySound(AUDIO,winsound.SND_FILENAME | winsound.SND_ASYNC)
def stop_music():
    winsound.PlaySound(None,winsound.SND_PURGE)

root=Tk()
root.title("Simple Music Player")
root.geometry("300x200")
root.configure(bg="#121212")

title=Label(root,text="Music")
title.pack(pady=20)

play_btn=Button(root,text="Play",command=play_music)
play_btn.pack(pady=10,ipadx=10,ipady=5)

stop_btn=Button(root,text="Stop",command=stop_music)
stop_btn.pack(pady=10,ipadx=10,ipady=5)

root.mainloop()
