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
from tkinter import messagebox

if __name__ == "__main__":

    def DeleteIdText():
        EnterIdText.delete(0, 'end')

    def DeleteNameText():
        EnterNameText.delete(0, 'end')

    def isNumber(entry):
        try:
            float(entry)
            return True
        except ValueError:
            pass

    def CaptureImages():
        Id = (EnterIdText.get())
        EnteredName = (EnterNameText.get())
        if(isNumber(Id) and EnteredName.isalpha()):
            cap = cv2.VideoCapture(0)
            harcascadeFilePath = "AllData\haarcascade_frontalface_default.xml"
            Facedetector = cv2.CascadeClassifier(harcascadeFilePath)
            TempNum = 0
            while(True):
                _, Image = cap.read()
                if(_ == False):
                    messagebox.showerror(title="Error", message="You have to close video running on home page or select image checkbox"
                                         )
                    root.destroy()
                    break

                grayImg = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
                Faces = Facedetector.detectMultiScale(grayImg, 1.3, 5)
                for (x, y, width, height) in Faces:
                    TempNum += 1
                    cv2.rectangle(Image, (x, y), (x+width, y+height),
                                  (255, 0, 0), 2)

                    cv2.imwrite("AllData\DataSetImages\ "+EnteredName + "."+Id + '.' +
                                str(TempNum) + ".jpg", grayImg[y:y+height, x:x+width])
                    cv2.imshow('Detecting the faces', Image)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif TempNum > 70:
                    break

            cap.release()
            cv2.destroyAllWindows()
            Result = "Images Saved [ ID : " + Id + \
                ", Name : " + EnteredName+" ]\n"
            ExcelRow = [Id, EnteredName]
            with open('AllData\StudentDataRecord.csv', 'a+') as CSVFile:
                w = csv.writer(CSVFile)
                w.writerow(ExcelRow)
            CSVFile.close()
            Messages.configure(text=Result)
        else:
            if(isNumber(EnteredName)):
                Result = "Please enter Alphabetical Name only."
                Messages.configure(text=Result)
            if(Id.isalpha()):
                Result = "Please enter Numeric Id only."
                Messages.configure(text=Result)

    def getImagesData(Imagepath):
        ImagesPath = [os.path.join(Imagepath, file)
                      for file in os.listdir(Imagepath)]
        FacesArray = []
        IdArray = []
        for path in ImagesPath:
            pilImage = Image.open(path).convert('L')
            imageNp = np.array(pilImage, 'uint8')
            Id = int(os.path.split(path)[-1].split(".")[1])
            IdArray.append(Id)
            FacesArray.append(imageNp)

        return FacesArray, IdArray

    def trainingImagesDataset():
        harcascadeFilePath = "AllData\haarcascade_frontalface_default.xml"
        Facedetector = cv2.CascadeClassifier(harcascadeFilePath)
        Facerecognizer = cv2.face_LBPHFaceRecognizer.create()
        Faces, Id = getImagesData("AllData\DataSetImages")
        Facerecognizer.train(Faces, np.array(Id))
        Facerecognizer.save("AllData\TrainedData\DataTrained.yml")
        Result = "Training of Images completed"
        Messages.configure(text=Result)

    root = tk.Tk()
    root.title("Train the Dataset")
    root.configure(background='gray5', bd=1, relief=SUNKEN,)
    root.minsize(920, 586)
    root.maxsize(920, 586)
    root.geometry('921x586')
    root.wm_iconbitmap('Webaly.ico')

    top_frame = Frame(root, bg='black', relief=SUNKEN)
    center = Frame(root, bg='black', relief=SUNKEN, bd=1)
    btm_frame = Frame(root, bg='black', relief=SUNKEN)

    top_frame.grid(row=0, sticky="ew")
    center.grid(row=1, sticky="nsew")
    btm_frame.grid(row=3, sticky="ew")

    headingLabel = tk.Label(top_frame, text="Attendance Management System",
                            bg="black", fg="white", relief=SUNKEN, width=48, height=4, font=('ComicSansMs', 23, 'italic bold'), anchor=CENTER)

    headingLabel.pack(fill=X)

    enterIDLabel = tk.Label(center, text="Enter your  ID", width=20, height=2,
                            fg="black", bg="yellow", font=('Verdana', 15, ' bold '), relief=SUNKEN)

    enterIDLabel.grid(row=0, column=0, padx=(5, 2),
                      pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

    EnterIdText = tk.Entry(center, width=25, bg="white",
                           fg="black", font=('Verdana', 15, ' bold '), relief=SUNKEN)

    EnterIdText.grid(row=0, column=1, padx=(5, 2),
                     pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

    EnterNameLabel = tk.Label(center, text="Enter your Name", width=20, fg="black",
                              bg="yellow", height=2, font=('Verdana', 15, ' bold '), relief=SUNKEN)

    EnterNameLabel.grid(row=1, column=0, padx=(5, 2),
                        pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

    EnterNameText = tk.Entry(center, width=20, bg="white",
                             fg="black", font=('Verdana', 15, ' bold '), relief=SUNKEN)

    EnterNameText.grid(row=1, column=1, padx=(5, 2),
                       pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

    Notification = tk.Label(center, text="Notifications -->", width=20, fg="black",
                            bg="yellow", height=2, font=('Verdana', 15, ' bold '), relief=SUNKEN)

    Notification.grid(row=2, column=0, padx=(5, 2),
                      pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

    Messages = tk.Label(center, text="", bg="white", fg="black",
                        width=22, font=('Verdana', 15, ' bold '), relief=SUNKEN)

    Messages.grid(row=2, column=1, padx=(5, 2),
                  pady=(15, 15), sticky=W+E+N+S, columnspan=2, rowspan=1)

    clearIdButton = tk.Button(center, text="Clear!!!", command=DeleteIdText, fg="black", bg="red",
                              width=20,  bd=2, activebackground="orange", font=('Verdana', 13, ' bold '), relief=SUNKEN)

    clearIdButton.grid(row=0, column=2, padx=(5, 2),
                       pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

    clearNameButton = tk.Button(center, text="Clear!!!", command=DeleteNameText, fg="black", bg="red",
                                bd=2, activebackground="orange", font=('Verdana', 13, ' bold '), relief=SUNKEN)

    clearNameButton.grid(row=1, column=2, padx=(5, 2),
                         pady=(15, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

    CaptureImgButton = tk.Button(center, text="Capture Images", command=CaptureImages, fg="black", bg="lime",
                                 bd=2, activebackground="Green", font=('Verdana', 13, ' bold '), relief=SUNKEN)

    CaptureImgButton.grid(row=4, column=0, padx=(15, 2),
                          pady=(55, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

    TrainImgButton = tk.Button(center, text="Train Images", command=trainingImagesDataset, fg="black",
                               bg="lime", bd=2, activebackground="Green", font=('Verdana', 13, ' bold '), relief=SUNKEN)

    TrainImgButton.grid(row=4, column=1, padx=(15, 2),
                        pady=(55, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

    QuitRoot = tk.Button(center, text="Exit", command=root.destroy, fg="black",
                         bg="red", height=3, bd=2, activebackground="orange", font=('times', 15, ' bold '))

    QuitRoot.grid(row=4, column=2, padx=(15, 2),
                  pady=(58, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

    Status = tk.Label(btm_frame, text="Designed by PDPM IIITDM 2018-batch, Group No: 6",
                      relief=SUNKEN, font="ComicSansMs 10", fg='linen', bg='black', bd=0.5, )

    Status.pack(fill=X, side=BOTTOM)

    root.mainloop()
