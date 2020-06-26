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


def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        pass


def CaptureImages(id, name):
    Id = id
    name = name
    if(isNumber(Id) and name.isalpha()):

        harcascadeFilePath = "AllData\haarcascade_frontalface_default.xml"
        FaceDetector = cv2.CascadeClassifier(harcascadeFilePath)
        sampleNum = 0

        f = tkinter.filedialog.askopenfile(mode='r')

        if f != None:
            img = Image.open(f.name)

            filename = ImageTk.PhotoImage(img)

            img = cv2.imread(f.name)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        while(True):

            grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = FaceDetector.detectMultiScale(grayImg, 1.3, 5)
            for (x, y, width, height) in faces:
                cv2.rectangle(img, (x, y), (x+width, y+height), (255, 0, 0), 2)
                temp = temp+1
                cv2.imwrite("AllData\DataSetImages\ "+name + "."+Id + '.' +
                            str(temp) + ".jpg", gray[y:y+height, x:x+width])
                cv2.imshow('Face Detecting', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif temp > 70:
                break

        cv2.destroyAllWindows()
        data = [Id, name]
        with open('AllData\StudentDataRecord.csv', 'a+') as filee:
            w = csv.writer(filee)
            w.writerow(data)
        filee.close()


if __name__ == "__main__":
    id = input("Enter  roll number or Id")
    name = input("Enter  name")
    CaptureImages(id, name)
