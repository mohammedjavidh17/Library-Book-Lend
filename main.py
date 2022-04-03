import modules, face_recognition
import cv2, time
import pandas as pd
from tkinter import * #For Gui
from PIL import Image, ImageTk 

Data = pd.read_csv("data.csv")
lst = list(Data.iloc[:, 0])
TrainedList = modules.Train(lst)
print("trained Succesfull")

#FontDetials
Font_Title = "Consolas"
Font_Text = "Consolas"

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
def PlotFace(img):
    try:
        loc = face_recognition.face_locations(img)[0]
        cv2.rectangle(img, (loc[0], loc[3]), (loc[2], loc[1]), (225,0,255), 2)
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

    def post_LendBook(results):
        pass

    for x in range(25, 0, -1):
        check, frame = cam.read()
        PlotFace(frame)
        #Rearrang the color channel
        b,g,r = cv2.split(frame)
        img = cv2.merge((r,g,b))
        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im) 
        for a in VideoFrame.winfo_children():
            a.destroy()
        # Put it in the display window
        Label(VideoFrame, text="Face Recognition", font=(Font_Title, 20)).pack()
        Label(VideoFrame, image=imgtk).pack()
        Label(VideoFrame, text=str(int(x/2.5)), font=(Font_Title, 20), fg='red').pack()
        root.update()
        if x > 45:
            continue
        result = modules.Test(frame, TrainedList)
        for buf in result:
            if buf:
                print(result)
                ind = []
                for val in range(len(result)):
                    if result[val]:
                        ind.append(val)
                name = str(Data.iloc[ind[0], 3]) + "\n" + str(Data.iloc[ind[0], 1])
                book = pd.read_csv("books.csv")
                print(book)
                for x in range(100, 0, -1):
                    detector = cv2.QRCodeDetector()
                    Chk, qrFrame = cam.read()
                    data, bbox, _ = detector.detectAndDecode(qrFrame)
                    b,g,r = cv2.split(qrFrame)
                    img = cv2.merge((r,g,b))
                    im = Image.fromarray(img)
                    imgtk = ImageTk.PhotoImage(image=im) 
                    for a in VideoFrame.winfo_children():
                        a.destroy()
                    # Put it in the display window
                    Label(VideoFrame, text="Welcome "+name, font=(Font_Title, 20)).pack()
                    Label(VideoFrame, text="Qr Code", font=(Font_Title, 20)).pack()
                    Label(VideoFrame, image=imgtk).pack()
                    Label(VideoFrame, text=str(int(x/10)), font=(Font_Title, 20), fg='red').pack()
                    root.update()
                    if str(data) != '':
                        book_ind = []
                        book_buf = book.iloc[:, -1].to_list()
                        for cd in range(len(book_buf)):
                            if str(book_buf[cd]) == str(data):
                                book_ind.append(cd)
                        if len(book_ind) == 0:
                            continue
                    post_LendBook(book_ind[0], ind[0])
                    cv2.waitKey(100)
                if x == 1:
                    for wid in VideoFrame.winfo_children():
                        wid.destroy()
                    root.update()
                    Label(VideoFrame, text="QR not found", font=(Font_Text, 25)).pack()
                    root.update()
                    time.sleep(2)
                    cam.release()
                    mainWindow()
                            
        root.update()
        if x == 1:
            for wid in VideoFrame.winfo_children():
                wid.destroy()
            root.update()
            Label(VideoFrame, text="Face not Recognized", font=(Font_Text, 25)).pack()
            root.update()
            time.sleep(2)
            mainWindow()


mainWindow()
root.mainloop()
