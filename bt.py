from tkinter import *
from PIL import Image,ImageTk

root=Tk()
root.title("Analytics")

pil_img=Image.open(r"C:\Users\guddu\OneDrive\Desktop\ft\btn.png")

pil_img=pil_img.resize((100,100))

img=ImageTk.PhotoImage(pil_img)

def onclick():
    print("Button clicked")

button=Button(root,image=img,text="Analytics",compound="left",font=("Times New Roman",20,"bold"),bg="black", fg="Aqua", command=onclick)
button.pack(side="top",padx=50,pady=20)

root.mainloop()
