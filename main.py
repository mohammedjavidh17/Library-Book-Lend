import modules
import cv2
import pandas as pd
from tkinter import * #For Gui
from PIL import Image, ImageTk 

#FontDetials
Font_Title = "Consolas"

#MainWindow
root = Tk() #Root
root.title("SRM CENTRAL LIBRARY")
width = root.winfo_screenwidth() - 50   
height = root.winfo_screenheight() - 50
root.geometry('%dx%d'%(width, height))          #setting the size of window

def clrScreen():                                #destroy all the widget in the root (often used)
    try:
        for x in root.winfo_children():
            x.destroy()
    except:
        pass

def mainWindow():  
    clrScreen()                             #MainWindow
    frame = LabelFrame(root)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.99, relheight=0.99)
    Button(frame,text="Go", command=LendBook).pack()

def LendBook():
    clrScreen()

    cam = cv2.VideoCapture(0)

    frm = LabelFrame(root) #MainFrame 
    frm.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.99, relheight=0.99)
    VideoFrame = Frame(frm) #Frame to display video
    VideoFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(frm, text="Welcome", font=(Font_Title, 30)).place(relx=0.5, rely=0.01, anchor=N) #Title

    for x in range(100):
        check, frame = cam.read()
        #Rearrang the color channel
        b,g,r = cv2.split(frame)
        img = cv2.merge((r,g,b))
        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im) 
        for a in VideoFrame.winfo_children():
            a.destroy()
        # Put it in the display window
        Label(VideoFrame, image=imgtk).pack()
        Label(VideoFrame, text=str(int(x/10))+" sec").pack()
        root.update()
        cv2.waitKey(100)


mainWindow()
root.mainloop()