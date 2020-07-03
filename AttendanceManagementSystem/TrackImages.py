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
from tkinter import messagebox

if __name__ == "__main__":

    def RecognizeImage():
        ImageRecognize = cv2.face.LBPHFaceRecognizer_create()
        ImageRecognize.read("AllData\TrainedData\DataTrained.yml")
        harcascadeFilePath = "AllData\haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadeFilePath)
        datafile = pd.read_csv("AllData\StudentDataRecord.csv")

        f = tkinter.filedialog.askopenfile(mode='r')

        if f != None:
            img = Image.open(f.name)
            filename = ImageTk.PhotoImage(img)
            img = cv2.imread(f.name)
            grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            collumn_names = ['Id', 'Name', 'Date', 'Time']
            AttendanceOfStudent = pd.DataFrame(columns=collumn_names)
            while True:

                faces = faceCascade.detectMultiScale(grayImg, 1.2, 6)
                for(x, y, width, height) in faces:
                    cv2.rectangle(
                        img, (x, y), (x+width, y+height), (225, 0, 0), 2)
                    Id, confidence = ImageRecognize.predict(
                        grayImg[y:y+height, x:x+width])
                    if(confidence <= 50):
                        CurrentTime = time.time()
                        dateTime = datetime.datetime.fromtimestamp(
                            CurrentTime).strftime('%Y-%m-%d')
                        timeValue = datetime.datetime.fromtimestamp(
                            CurrentTime).strftime('%H:%M:%S')
                        name = datafile.loc[datafile['Id']
                                            == Id]['Name'].values
                        key = str(Id)+"-"+name
                        AttendanceOfStudent.loc[len(AttendanceOfStudent)] = [
                            Id, name, dateTime, timeValue]

                    else:
                        Id = 'Unknown'
                        key = str(Id)

                    cv2.putText(img, str(key), (x, y+height),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (20, 210, 10), 2)
                AttendanceOfStudent = AttendanceOfStudent.drop_duplicates(
                    subset=['Id'], keep='first')

                cv2.imshow('Recognizing Faces', img)

                if cv2.waitKey(10000) or cv2.waitKey(1) == ord('q'):
                    cv2.destroyWindow('Face Recognizing')
                    break

        CurrentTime = time.time()
        CurrentDate = datetime.datetime.fromtimestamp(
            CurrentTime).strftime('%Y-%m-%d')
        timeValue = datetime.datetime.fromtimestamp(
            CurrentTime).strftime('%H:%M:%S')
        Hour, Minute, Second = timeValue.split(":")

        AttendancefileName = "AllData\StudentAttendance\StudentAttendance_" + \
            CurrentDate+"_"+Hour+"-"+Minute+".csv"
        AttendanceOfStudent.to_csv(AttendancefileName, index=False)
        Firebase = pyrebase.initialize_app(firebaseConfig)
        Databasestorage = Firebase.storage()
        BlobStorage = Databasestorage.child(
            'uploads/' + AttendancefileName).put(AttendancefileName)
        StudentData = {'name': "Date_"+CurrentDate+"  Time_"+Hour+"-"+Minute+"-"+Second,
                       'url': "https://firebasestorage.googleapis.com/v0/b/ <gs://python-firebasesdkinteexample.appspot.com> %2FAttendance%5CAttendance_" +
                       CurrentDate+"_"+Hour+"-"+Minute +
                       ".csv?alt=media&token="+BlobStorage['downloadTokens']

                       }
        UploadDataToDatabase = firebase.post('/uploads', StudentData)
        retrivedData = AttendanceOfStudent
        StudentsPresent.configure(text=retrivedData)

        cv2.destroyAllWindows()

    def RecognizeFaceFromVideo():
        FaceRecognize = cv2.face.LBPHFaceRecognizer_create()
        FaceRecognize.read("AllData\TrainedData\DataTrained.yml")
        harcascadeFilePath = "AllData\haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadeFilePath)
        datafile = pd.read_csv("AllData\StudentDataRecord.csv")
        collum_names = ['Id', 'Name', 'Date', 'Time']
        AttendanceOfStudent = pd.DataFrame(columns=collum_names)

        cap = cv2.VideoCapture(0)
        if(cap.isOpened() == False):
            messagebox.showerror(title="Error", message="There is some problem with your camera"
                                 )
            root.destroy()

        while True:
            _, img = cap.read()
            if(_ == False):
                messagebox.showerror(title="Error", message="You have to close video running on home page or select image checkbox"
                                     )
                root.destroy()
                break

            grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            Detectedfaces = faceCascade.detectMultiScale(grayImg, 1.2, 5)
            for(x, y, width, height) in Detectedfaces:
                cv2.rectangle(img, (x, y), (x+width, y+height), (225, 0, 0), 2)
                Id, confidence = FaceRecognize.predict(
                    grayImg[y:y+height, x:x+width])
                if(confidence <= 50):
                    CurrentTime = time.time()
                    CurrentDate = datetime.datetime.fromtimestamp(
                        CurrentTime).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(
                        CurrentTime).strftime('%H:%M:%S')
                    name = datafile.loc[datafile['Id'] == Id]['Name'].values
                    key = str(Id)+"-"+name
                    AttendanceOfStudent.loc[len(AttendanceOfStudent)] = [
                        Id, name, CurrentDate, timeStamp]

                else:
                    Id = 'Unknown'
                    key = str(Id)

                cv2.putText(img, str(key), (x, y+height),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            AttendanceOfStudent = AttendanceOfStudent.drop_duplicates(
                subset=['Id'], keep='first')

            cv2.imshow('Face Recognizing', img)

            if cv2.waitKey(10000) or cv2.waitKey(1) == ord('q'):

                break

        CurrentTime = time.time()
        CurrentDate = datetime.datetime.fromtimestamp(
            CurrentTime).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(
            CurrentTime).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")

        fileName = "AllData\StudentAttendance\StudentAttendance_" + \
            CurrentDate+"_"+Hour+"-"+Minute+".csv"
        AttendanceOfStudent.to_csv(fileName, index=True)
        Firebase = pyrebase.initialize_app(firebaseConfig)
        storage = Firebase.storage()
        bllob = storage.child('uploads/' + fileName).put(fileName)

        StudentData = {'name': "Date: "+CurrentDate+" Time: "+Hour+"-"+Minute+"--"+Second, 'url': "https://firebasestorage.googleapis.com/v0/b/ <gs://fir-demo-cc179.appspot.com/> %2FAttendance%5CAttendance_" +
                       CurrentDate+"_"+Hour+"-"+Minute+".csv?alt=media&token="+bllob['downloadTokens']}

        UploadDataToDatabase = firebase.post('/uploads', StudentData)
        retrivedData = AttendanceOfStudent
        StudentsPresent.configure(text=retrivedData)
        cap.release()
        cv2.destroyAllWindows()

    firebaseConfig = {
        "apiKey": "Enter your api key here ",
        "authDomain": "enter auth domain here ",
        "databaseURL": "enter your database url",
        "projectId": "...",
        "storageBucket": "..",
        "messagingSenderId": "..",
        "appId": "...",
        "measurementId": ".."
    }

    firebase = firebase.FirebaseApplication(
        "database url", None)
    BlobStorage = Blob.from_string(
        "gs:storage url")

    root = tk.Tk()
    root.title("Track Data")
    root.configure(background='gray5', bd=1, relief=SUNKEN,)
    root.minsize(728, 528)
    root.maxsize(728, 528)
    root.geometry('728x528')
    root.wm_iconbitmap('Webaly.ico')

    top_frame = Frame(root, bg='black', relief=SUNKEN)
    center = Frame(root, bg='black', relief=SUNKEN, bd=1)
    btm_frame = Frame(root, bg='black', relief=SUNKEN)

    top_frame.grid(row=0, sticky="ew")
    center.grid(row=1, sticky="nsew")
    btm_frame.grid(row=3, sticky="ew")

    headingLabel = tk.Label(top_frame, text="Attendance Management System",
                            bg="black", fg="white", relief=SUNKEN, height=2, font=('Verdana', 25, 'italic bold'), anchor=CENTER)
    headingLabel .pack(fill=X)

    ListLabel = tk.Label(center, text="** List Of Students Present  in Class **",
                         relief=SUNKEN,  fg="black", bg="white", height=2, font=('Verdana', 15, ' bold'))

    ListLabel.grid(row=0, column=0, padx=(5, 2),
                   pady=(15, 15), sticky=W+E+N+S, columnspan=3, rowspan=1)

    StudentsPresent = tk.Label(center, text="", fg="black", bg="white",
                               activeforeground="green", height=11, font=('Verdana', 13, ' bold '), relief=SUNKEN)

    StudentsPresent.grid(row=1, column=0, padx=(5, 2),
                         pady=(15, 15), sticky=W+E+N+S, columnspan=3, rowspan=1)

    RecognizeFaceFromPic = tk.Button(center, text="Track Image: from picture", command=RecognizeImage, fg="black", bg="yellow",
                                     relief=SUNKEN,  activebackground="orange", font=('Verdana', 15, ' bold '))

    RecognizeFaceFromPic.grid(row=3, column=0, padx=(5, 2),
                              pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

    RecognizeFaceFromVideo = tk.Button(center, text="Track Image: from camera", command=RecognizeFaceFromVideo, fg="black", bg="orange", relief=SUNKEN,
                                       activebackground="Yellow", font=('Verdana', 15, ' bold '))
    RecognizeFaceFromVideo.grid(row=3, column=1, padx=(5, 2),
                                pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

    Exit = tk.Button(center, text="Quit", command=root.destroy, fg="black",
                     bg="red", activebackground="orange", font=('Verdana', 12, ' bold '), relief=SUNKEN)
    Exit.grid(row=3, column=2, padx=(15, 2),
              pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

    Status = tk.Label(btm_frame, text="Desigend by IIITDM PDPM 2018-Batch, Group-No: 6",
                      width=80, fg="white", bg="black", font=('Verdana', 10, ' bold'), relief=SUNKEN)

    Status.pack(fill=X)

    root.mainloop()
