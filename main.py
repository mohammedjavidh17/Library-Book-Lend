import modules, face_recognition
import cv2, time
from datetime import date
import pandas as pd
from tkinter import messagebox
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
    Button(frame,text="Go1", command=Returnbook).pack()

def LendBook():
    clrScreen()

    cam = cv2.VideoCapture(0)

    frm = LabelFrame(root) #MainFrame 
    frm.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.99, relheight=0.99)
    VideoFrame = Frame(frm) #Frame to display video
    VideoFrame.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    Label(frm, text="Welcome", font=(Font_Title, 30)).place(relx=0.5, rely=0.01, anchor=N) #Title

    def post_LendBook(data, a ,df_book): #[book_ind[0], str(data), ind[0]]
        def ConfrimAdd(df):
            loc = "BookLend.csv"
            df.to_csv(loc, index=False, mode = 'a', columns = None, header = False)
            mainWindow()
            root.update()
            messagebox.showinfo('Succesfull', "Process Sucessfull.!\nThankYou for using Me")
            
        today = date.today()
        todaysDate = today.strftime("%d/%m/%Y")         #PersonId ,Code, LendDate
        Lend_list = [                                   
            data[-1], data[0], str(todaysDate)
        ]
        df_Lend = pd.DataFrame([Lend_list], columns=('PersonId' ,'Code', 'LendDate'))
        for wid in VideoFrame.winfo_children():
            wid.destroy()
        stu_ind = data[-1]
        bk_ind = data[0]
        Name = str(Data.iloc[stu_ind, 3])
        RegNo= str(Data.iloc[stu_ind, 1])
        bookName = str(df_book.iloc[bk_ind, 0])
        Label(VideoFrame, text="Lend Information", font=(Font_Title, 35)).pack()
        Label(VideoFrame, text="Name : "+Name, font=(Font_Text, 25)).pack()
        Label(VideoFrame, text="RegNo : "+RegNo, font=(Font_Text, 25)).pack()
        Label(VideoFrame, text="Book : "+bookName, font=(Font_Text, 25)).pack()
        Label(VideoFrame, text="Date :" +todaysDate, font=(Font_Text, 25)).pack()
        Button(VideoFrame, text="Confirm", font=(Font_Text, 25), command=lambda: ConfrimAdd(df_Lend)).pack()
        Button(VideoFrame, text="Cancel", font=(Font_Text, 25), command=mainWindow).pack()

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
                        cam.release()
                        post_LendBook([book_ind[0], str(data), ind[0]], Data, book) 
                        
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
def Returnbook():
    clrScreen()
    frame = LabelFrame(root)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.99, relheight=0.99)
    frameTr = Frame(frame)
    frameTr.place(relx=0.5, rely=0.5, anchor=CENTER)
    tr = modules.TableDis([], ("RegNo", "Name", "Phone", "Mail", "Book Code", "Book Name", "Lend Date"), 30, frameTr, False, 180)
    df_Lend = pd.read_csv("BookLend.csv")
    df_book = pd.read_csv("books.csv")
    df_data = pd.read_csv("data.csv")
    def remove():
        Lend_indx = []
        for b in tr.selection():
            lst = list(tr.item(b)['values'])
            regNo = str(lst[0])
            bokCode = int(lst[-3])
            repStu_ind = list(df_data.index[df_data.iloc[:, 1] == regNo])[0]
            repBok_ind = list(df_book.index[df_book.iloc[:, -1] == bokCode])[0]
            df_buf = df_Lend[df_Lend.iloc[:, 0] == repStu_ind]
            val= list(df_buf.index[df_buf.iloc[:, 1] == repBok_ind])[0]
            df_Lend.drop(labels=[val], axis=0, inplace=True)
            loc = 'BookLend.csv'
            df_Lend.to_csv(loc, index=False, mode = 'w', columns = None, header = True)
            Returnbook()

    for x in range(df_Lend.shape[0]):
        to_dis_list = []
        stu_ind = int(df_Lend.iloc[x, 0])
        bok_ind = int(df_Lend.iloc[x, 1])
        stu_name = str(df_data.iloc[stu_ind, 3])
        stu_reg = str(df_data.iloc[stu_ind, 1])
        stu_phone= str(df_data.iloc[stu_ind, -2])
        stu_mail = str(df_data.iloc[stu_ind, -1])
        bok_name = str(df_book.iloc[bok_ind, 0])
        bok_code = str(df_book.iloc[bok_ind, -1])
        lendat = str(df_Lend.iloc[x, -1])
        lst = [stu_reg, stu_name, stu_phone, stu_mail, bok_code, bok_name, lendat]
        to_dis_list.append(lst)
        df = pd.DataFrame(to_dis_list)
        modules.TableApp(df, tr, False)
    Button(frame, text= "Remove", font=(Font_Text, 20), command=remove).place(relx=0.025, rely=0.025, anchor=NW)
    Button(frame, text="Back", font=(Font_Text, 20), command=mainWindow).place(relx=0.975, rely=0.025, anchor=NE)
    
    

mainWindow()
root.mainloop()
