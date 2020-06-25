import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import Message, Text
from cv2 import cv2
import os
import csv
import numpy as np
from PIL import Image, ImageTk
import tkinter.font as font

window = tk.Tk()
window.title("Train data ")
window.configure(background='gray5', bd=1, relief=SUNKEN,)
window.minsize(929, 586)
window.maxsize(929, 586)
window.geometry('929x586')
window.wm_iconbitmap('Webaly.ico')

top_frame = Frame(window, bg='black', relief=SUNKEN)
center = Frame(window, bg='black', relief=SUNKEN, bd=1)
btm_frame = Frame(window, bg='black', relief=SUNKEN)

top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
btm_frame.grid(row=3, sticky="ew")

lbl = tk.Label(top_frame, text="Attendance Management System",
               bg="black", fg="white", relief=SUNKEN, width=40, height=3, font=('times', 30, 'italic bold'), anchor=CENTER)
# lbl.place(x=100, y=20)
lbl.pack(fill=X)

lbl1 = tk.Label(center, text="Enter ID", width=20, height=2,
                fg="black", bg="yellow", font=('Verdana', 15, ' bold '), relief=SUNKEN)
# lbl1.place(x=200, y=200)
lbl1.grid(row=0, column=0, padx=(5, 2),
          pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

txt1 = tk.Entry(center, width=25, bg="white",
                fg="black", font=('Verdana', 15, ' bold '), relief=SUNKEN)
# txt1.place(x=550, y=215)
txt1.grid(row=0, column=1, padx=(5, 2),
          pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)


lbl2 = tk.Label(center, text="Enter Name", width=20, fg="black",
                bg="yellow", height=2, font=('Verdana', 15, ' bold '), relief=SUNKEN)
# lbl2.place(x=200, y=300)
lbl2.grid(row=1, column=0, padx=(5, 2),
          pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

txt2 = tk.Entry(center, width=20, bg="white",
                fg="black", font=('Verdana', 15, ' bold '), relief=SUNKEN)
# txt2.place(x=550, y=315)
txt2.grid(row=1, column=1, padx=(5, 2),
          pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)


lbl3 = tk.Label(center, text="Notification →", width=20, fg="black",
                bg="yellow", height=2, font=('Verdana', 15, ' bold '), relief=SUNKEN)
# lbl3.place(x=200, y=400)
lbl3.grid(row=2, column=0, padx=(5, 2),
          pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)


message = tk.Label(center, text="", bg="white", fg="black",
                   width=20, height=2, font=('Verdana', 15, ' bold '), relief=SUNKEN)
# message.place(x=550, y=400)
message.grid(row=2, column=1, padx=(5, 2),
             pady=(15, 15), sticky=W+E+N+S, columnspan=2, rowspan=1)


def clearId():
    txt1.delete(0, 'end')


def clearName():
    txt2.delete(0, 'end')


def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        pass


def takeImages():
    Id = (txt1.get())
    name = (txt2.get())
    if(isNumber(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                sampleNum = sampleNum+1
                cv2.imwrite("SampleImages\ "+name + "."+Id + '.' +
                            str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                cv2.imshow('Face Detecting', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 60:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id + " Name : " + name
        row = [Id, name]
        with open('StudentRecord.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text=res)
    else:
        if(isNumber(name)):
            res = "Enter Alphabetical Name"
            message.configure(text=res)
        if(Id.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text=res)


def trainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = getImagesAndLabels("SampleImages")
    recognizer.train(faces, np.array(Id))
    recognizer.save("DataSet\Trainner.yml")
    res = "Image Trained"
    message.configure(text=res)


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


clearButton1 = tk.Button(center, text="Clear", command=clearId, fg="black", bg="red",
                         width=20, height=2, activebackground="orange", font=('Verdana', 13, ' bold '), relief=SUNKEN)
# clearButton1.place(x=850, y=200)
clearButton1.grid(row=0, column=2, padx=(5, 2),
                  pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)


clearButton2 = tk.Button(center, text="Clear", command=clearName, fg="black", bg="red",
                         width=20, height=2, activebackground="orange", font=('Verdana', 13, ' bold '), relief=SUNKEN)
# clearButton2.place(x=850, y=300)
clearButton2.grid(row=1, column=2, padx=(5, 2),
                  pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)


takeImg = tk.Button(center, text="Take Images", command=takeImages, fg="black", bg="lime",
                    width=20, height=3, activebackground="Green", font=('Verdana', 13, ' bold '), relief=SUNKEN)
# takeImg.place(x=200, y=500)
takeImg.grid(row=4, column=0, padx=(15, 2),
             pady=(55, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)


trainImg = tk.Button(center, text="Train Images", command=trainImages, fg="black",
                     bg="lime", width=20, height=3, activebackground="Green", font=('Verdana', 13, ' bold '), relief=SUNKEN)
# trainImg.place(x=500, y=500)
trainImg.grid(row=4, column=1, padx=(15, 2),
              pady=(55, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)


quitWindow = tk.Button(center, text="Quit", command=window.destroy, fg="black",
                       bg="red", width=20, height=3, activebackground="orange", font=('times', 15, ' bold '))
# quitWindow.place(x=800, y=500)
quitWindow.grid(row=4, column=2, padx=(15, 2),
                pady=(58, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)


lbl4 = tk.Label(btm_frame, text="DESIGN BY PDPM IIITDM BATCH 2018, GROUP NO : 6",
                relief=SUNKEN, font="ComicSansMs 10", fg='linen', bg='black', bd=0.5, )
# lbl4.place(x=200, y=620)
lbl4.pack(fill=X, side=BOTTOM)

window.mainloop()
