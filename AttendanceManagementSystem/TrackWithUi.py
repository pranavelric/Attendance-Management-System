import tkinter as tk
from tkinter import Message, Text
from cv2 import cv2
import os
import csv
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyrebase
from tkinter import ttk
from tkinter import *
from firebase import firebase
from google.cloud import storage
from google.cloud.storage.blob import Blob
import tkinter.filedialog
from PIL import Image, ImageTk

window = tk.Tk()
window.title("Track Data")
window.configure(background='gray5', bd=1, relief=SUNKEN,)
window.minsize(728, 528)
window.maxsize(728, 528)
window.geometry('728x528')
window.wm_iconbitmap('Webaly.ico')

top_frame = Frame(window, bg='black', relief=SUNKEN)
center = Frame(window, bg='black', relief=SUNKEN, bd=1)
btm_frame = Frame(window, bg='black', relief=SUNKEN)


top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
btm_frame.grid(row=3, sticky="ew")

lbl = tk.Label(top_frame, text="Attendance Management System",
               bg="black", fg="white", relief=SUNKEN, width=30, height=3, font=('times', 30, 'italic bold'), anchor=CENTER)
# lbl.place(x=100, y=20)
lbl.pack(fill=X)

lbl1 = tk.Label(center, text="↓  List Of Present Students  ↓", width=25,
                relief=SUNKEN,  fg="black", bg="white", height=2, font=('Verdana', 15, ' bold'))
# lbl1.place(x=540, y=320)
lbl1.grid(row=0, column=0, padx=(5, 2),
          pady=(15, 15), sticky=W+E+N+S, columnspan=3, rowspan=1)


message = tk.Label(center, text="", fg="black", bg="white",
                   activeforeground="green", width=35, height=7, font=('times', 15, ' bold '), relief=SUNKEN)
# message.place(x=470, y=400)
message.grid(row=1, column=0, padx=(5, 2),
             pady=(15, 15), sticky=W+E+N+S, columnspan=3, rowspan=1)


config = {
    "apiKey": "AIzaSyABckEgLXuIltOAfKIjBH4paT3oimwelKI",
    "authDomain": "python-firebasesdkinteexample.firebaseapp.com",
    "databaseURL": "https://python-firebasesdkinteexample.firebaseio.com",
    "projectId": "python-firebasesdkinteexample",
    "storageBucket": "python-firebasesdkinteexample.appspot.com",
    "messagingSenderId": "687025953277",
    "appId": "1:687025953277:web:cafc0f5714677498562194",
    "measurementId": "G-C426GLDT23"
}

firebase = firebase.FirebaseApplication(
    "https://python-firebasesdkinteexample.firebaseio.com/", None)
blob = Blob.from_string("gs://python-firebasesdkinteexample.appspot.com")


def trackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("DataSet\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("StudentRecord.csv")

    f = tkinter.filedialog.askopenfile(mode='r')

    if f != None:
        img = Image.open(f.name)

        filename = ImageTk.PhotoImage(img)

        img = cv2.imread(f.name)
        # imgg, count = img_detect(img, faceCascade)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    while True:
        # ret, im = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 6)
        for(x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if(conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values
                tt = str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]

            else:
                Id = 'Unknown'
                tt = str(Id)
            if(conf > 75):
                noOfFile = len(os.listdir("UnknownImages"))+1
                cv2.imwrite("UnknownImages\Image"+str(noOfFile) +
                            ".jpg", img[y:y+h, x:x+w])
            cv2.putText(img, str(tt), (x, y+h), font, 1, (20, 210, 10), 2)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')

        cv2.imshow('Face Recognizing', img)
        pass

        if cv2.waitKey(10000) or cv2.waitKey(1) == ord('q'):
            cv2.destroyWindow('Face Recognizing')
            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")

    # fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    fileName = "Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+".csv"
    attendance.to_csv(fileName, index=False)
    Firebase = pyrebase.initialize_app(config)
    storage = Firebase.storage()
    blob = storage.child('uploads/' + fileName).put(fileName)
    # jay = storage.child().get_url(blob['downloadTokens'])

    data = {'name': "Date_"+date+"  Time_"+Hour+"-"+Minute+"-"+Second, 'url': "https://firebasestorage.googleapis.com/v0/b/ <gs://python-firebasesdkinteexample.appspot.com> %2FAttendance%5CAttendance_" +
            date+"_"+Hour+"-"+Minute+".csv?alt=media&token="+blob['downloadTokens']}
    # data =  { 'name': "Date_"+date+"  Time_"+Hour+"-"+Minute+"-"+Second, 'url': jay}
    result = firebase.post('/uploads', data)
    print(result)

    # cam.release()

    cv2.destroyAllWindows()

    res = attendance
    message.configure(text=res)


def trackImagesVideo():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("DataSet\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("StudentRecord.csv")

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if(conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values
                tt = str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]

            else:
                Id = 'Unknown'
                tt = str(Id)
            if(conf > 75):
                noOfFile = len(os.listdir("UnknownImages"))+1
                cv2.imwrite("UnknownImages\Image"+str(noOfFile) +
                            ".jpg", im[y:y+h, x:x+w])
            cv2.putText(im, str(tt), (x, y+h), font, 1, (255, 255, 255), 2)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')

        cv2.imshow('Face Recognizing', im)
        pass

        if cv2.waitKey(10000) or cv2.waitKey(1) == ord('q'):

            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")

    # fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    fileName = "Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+".csv"
    attendance.to_csv(fileName, index=False)
    Firebase = pyrebase.initialize_app(config)
    storage = Firebase.storage()
    blob = storage.child('uploads/' + fileName).put(fileName)
    # jay = storage.child().get_url(blob['downloadTokens'])

    data = {'name': "Date_"+date+"  Time_"+Hour+"-"+Minute+"-"+Second, 'url': "https://firebasestorage.googleapis.com/v0/b/ <gs://fir-demo-cc179.appspot.com/> %2FAttendance%5CAttendance_" +
            date+"_"+Hour+"-"+Minute+".csv?alt=media&token="+blob['downloadTokens']}
    # data =  { 'name': "Date_"+date+"  Time_"+Hour+"-"+Minute+"-"+Second, 'url': jay}
    result = firebase.post('/uploads', data)
    print(result)

    cam.release()
    cv2.destroyAllWindows()

    res = attendance
    message.configure(text=res)


trackImg = tk.Button(center, text="Track Image: from picture", command=trackImages, fg="black", bg="yellow",
                     relief=SUNKEN,  activebackground="orange", font=('Verdana', 15, ' bold '))
# trackImg.place(x=400, y=200)
trackImg.grid(row=3, column=0, padx=(5, 2),
              pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)


trackImgVideo = tk.Button(center, text="Track Image: from camera", command=trackImagesVideo, fg="black", bg="orange", relief=SUNKEN,
                          activebackground="Yellow", font=('Verdana', 15, ' bold '))
# trackImgVideo.place(x=400, y=300)
trackImgVideo.grid(row=3, column=1, padx=(5, 2),
                   pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)


quitWindow = tk.Button(center, text="Quit", command=window.destroy, fg="black",
                       bg="red", activebackground="orange", font=('times', 15, ' bold '), relief=SUNKEN)
# quitWindow.place(x=700, y=200)
quitWindow.grid(row=3, column=2, padx=(15, 2),
                pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)


lbl3 = tk.Label(btm_frame, text="DESIGN BY IIITDM PDPM BATCH 2018, GROUP NO : 6",
                width=80, fg="white", bg="black", font=('Verdana', 10, ' bold'), relief=SUNKEN)
# lbl3.place(x=200, y=620)
lbl3.pack(fill=X)


window.mainloop()
