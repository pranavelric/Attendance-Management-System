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


def takeImages():
    Id = "22"
    name = "Vaibhav"
    if(isNumber(Id) and name.isalpha()):
        # cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        f = tkinter.filedialog.askopenfile(mode='r')

        if f != None:
            img = Image.open(f.name)

            filename = ImageTk.PhotoImage(img)

            img = cv2.imread(f.name)
            # imgg, count = img_detect(img, faceCascade)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        while(True):
            # ret, img = cam.read()
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
        # cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id + " Name : " + name
        row = [Id, name]
        with open('StudentRecord.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()


if __name__ == "__main__":
    takeImages()
