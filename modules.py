import face_recognition
import numpy as np
from tkinter import *
import pandas as pd
import random, string
from tkinter import ttk
import cv2

def Train(images):                  #images arg (List of location of imageData of students)
    encodedList = []  
    for x in images:
        img = face_recognition.load_image_file(x)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encd = face_recognition.face_encodings(img)[0]
        encodedList.append(encd)    #encode the image and add it to a list
    return encodedList              #returns the encoded list

def Test(img, trainedList):                      
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    try:
        encoed = face_recognition.face_encodings(img)[0]
        results = face_recognition.compare_faces(trainedList, encoed)
        return results
    except:
        return []

def TableDel(tr):
    for x in tr.get_children():
        tr.delete(x)
def TableFetch(tr, clm):
    lst = []
    for x in tr.get_children():
        lst.append(tr.item(x)['values'])
    return pd.DataFrame(lst, columns=clm)
def TableApp(dt, tr, uniq):   #data, tree, unique append (True/ False)
    lst = []
    lst1 = []
    dtc = dt
    if uniq:
        for x in tr.get_children():
            lst.append(list(tr.item(x)['values']))

        for x in range(dt.shape[0]):
            if list(dt.iloc[x]) not in lst:
                lst1.append(list(dt.iloc[x]))
        dtc = pd.DataFrame(lst1)
        

    for x in range(dtc.shape[0]):
        # generating random strings 

        print("hell")
        res = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 10))
        tr.insert(parent='',index='end', iid=str(res), values=tuple(dtc.iloc[x]), text='')
        break           
def TableDis(dt, column_name, max_ht, rt, app, wid):    #Tree view creater
    
    w = ttk.Scrollbar(rt)
    w.pack(side=RIGHT, fill = 'y')
    tr = ttk.Treeview(rt, yscrollcommand=w.set)
    tr['columns'] = column_name
    tr.column('#0', minwidth=0, width=0)
    for x in range(len(column_name)):
        id = '#'+str(x+1)
        tr.column(id, anchor=W, width=wid)
    for x in column_name:
        tr.heading(x, text = x, anchor=W)
    tr['height'] = max_ht
    if app:
        for x in range(dt.shape[0]):
            # generating random strings 
            while(True):
                try:
                    res = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 10))
                    tr.insert(parent='',index='end', iid=str(res), values=tuple(dt.iloc[x]), text='')
                    break
                except:
                    pass
    tr.pack()
    w.config(command=tr.yview)
    return tr
